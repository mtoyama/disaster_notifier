import logging
import asyncio
import datetime
import time
import json
import sys
import os
from src.data_sources import nws_alerts, usgs, register
from src.data_sources.base import Status
from src.config import user
from src.config import trigger_earthquake
from src.config import trigger_weather_alert
from src import utils, timing, message_formatting

LOGGER = logging.getLogger(__name__)
CONFIG = "./user_config.json"
LOOP_INTERVAL = 60

async def gather_async_register_funcs(usgs_data,
                                      nws_alerts_data,
                                      dicts_list,
                                      triggers_usgs,
                                      triggers_nws_alerts):

    coros = []
    for func_dict in dicts_list:
        coros.append(
            func_dict["func"](
            *arrange_register_func_args(
                usgs_data,
                nws_alerts_data,
                func_dict,
                triggers_usgs,
                triggers_nws_alerts,
                )
            )
        )
    await asyncio.gather(*coros)

def arrange_register_func_args(usgs_data,
                               nws_alerts_data,
                               func_dict,
                               triggers_usgs,
                               triggers_nws_alerts):
    args = []
    if func_dict["class"] == usgs.USGSEarthquakeData:
        args.append(usgs_data)
        triggers = triggers_usgs
    elif func_dict["class"] == nws_alerts.NWSAlertsData:
        args.append(nws_alerts_data)
        triggers = triggers_nws_alerts

    if func_dict["triggers"] is True:
        args.append(triggers)

    return args

@timing.log_run_duration
def run_async_register_funcs(usgs_data,
                             nws_alerts_data,
                             dicts_list,
                             triggers_usgs,
                             triggers_nws_alerts):
    asyncio.run(gather_async_register_funcs(
        usgs_data,
        nws_alerts_data,
        dicts_list,
        triggers_usgs,
        triggers_nws_alerts
        )
    )

@timing.log_run_duration
def run_serial_register_funcs(usgs_data,
                              nws_alerts_data,
                              dicts_list,
                              triggers_usgs,
                              triggers_nws_alerts):
    for func_dict in dicts_list:
        func_dict["func"](
            *arrange_register_func_args(
                usgs_data,
                nws_alerts_data,
                func_dict,
                triggers_usgs,
                triggers_nws_alerts,
            )
        )

@timing.log_run_duration
def run_event_actions(data_sources, events_map):
    for data_source in data_sources:
        if data_source.status is not Status.FILTER_COMPLETED:
            continue
        if data_source.__class__ == usgs.USGSEarthquakeData:
            formatter = message_formatting.format_sms_earthquake
        elif data_source.__class__ == nws_alerts.NWSAlertsData:
            formatter = message_formatting.format_sms_nws_alert
        for key, value in data_source.get_payload().items():
            event = events_map[key]
            LOGGER.debug(f"Event: {event.summary}")
            LOGGER.debug(f"Payload value: {value}")
            if len(value) == 0:
                LOGGER.info(f"No data present in payload for event {event.summary}")
                continue
            if event.send_message_action:
                LOGGER.info(f"Sending SMS message for event {event.summary}")
                event.send_message_action.send_message(
                    formatter(
                        event.summary,
                        value
                    )
                )
                                

def main():
    nws_alerts_data = nws_alerts.NWSAlertsData()
    usgs_data = usgs.USGSEarthquakeData()

    with open(CONFIG, 'r') as config_file:
        json_data = json.load(config_file)

    config_users = []
    for user_dict in json_data["users"]:
        config_users.append(user.User(json_dict=user_dict))

    events_map = {}
    triggers_usgs = []
    triggers_nws_alerts = []
    for config_user in config_users:
        for event in config_user.events:
            events_map[event.id] = event
            if event.trigger.__class__ == trigger_earthquake.EarthquakeTrigger:
                triggers_usgs.append(event.trigger)
            elif event.trigger.__class__ == trigger_weather_alert.WeatherAlertTrigger:
                triggers_nws_alerts.append(event.trigger)

    data_sources = [usgs_data, nws_alerts_data]
    try:
        while True:
            index = 0
            data_source_process_start = datetime.datetime.now()
            while index < register.SourceRegister.get_long_pole_count():
                async_func_dicts, serial_func_dicts = register.SourceRegister.\
                    get_actions_by_async_at_index(index)

                run_async_register_funcs(
                    usgs_data, 
                    nws_alerts_data, 
                    async_func_dicts, 
                    triggers_usgs,
                    triggers_nws_alerts
                )

                run_serial_register_funcs(
                    usgs_data, 
                    nws_alerts_data, 
                    serial_func_dicts, 
                    triggers_usgs,
                    triggers_nws_alerts
                ) 
                index += 1
            data_source_process_duration = datetime.datetime.now() - data_source_process_start
            data_source_process_duration_s = data_source_process_duration.total_seconds()
            LOGGER.info(f"Data source process execution duration: {data_source_process_duration_s}")
            
            run_event_actions(data_sources, events_map)
            LOGGER.info(f"Processing complete. Sleeping for {LOOP_INTERVAL}s")
            time.sleep(LOOP_INTERVAL)
    finally:
        LOGGER.warning("Server shutting down!")
        for data_source in data_sources:
            data_source.cache_filter_list()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()