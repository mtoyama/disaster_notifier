import logging
import asyncio
import json
import sys
import os
from src.data_sources import nws_alerts, usgs
from src.data_sources.base import Status
from src.config import user
from src.config import trigger_earthquake
from src.config import trigger_weather_alert
from src import utils

LOGGER = logging.getLogger(__name__)
CONFIG = "./user_config.json"

async def gather_async_register_funcs(usgs_data,
                                      nws_alerts_data,
                                      dicts_list,
                                      triggers_usgs,
                                      triggers_nws_alerts):
    for func_dict in dicts_list:
        await asyncio.gather(func_dict["func"](
            *arrange_register_func_args(
                usgs_data,
                nws_alerts_data,
                func_dict,
                triggers_usgs,
                triggers_nws_alerts,
                )
            )
        )

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

def arrange_register_func_args(usgs_data,
                               nws_alerts_data,
                               func_dict,
                               triggers_usgs,
                               triggers_nws_alerts):
    args = []
    if func_dict["func"].__self__.__class__ == usgs.USGSEarthquakeData:
        triggers = triggers_usgs
    elif func_dict["func"].__self__.__class__ == nws_alerts.NWSAlertsData:
        triggers = triggers_nws_alerts

    if func_dict["triggers"] is True:
        args.append(triggers)

    LOGGER.info(args)
    return args
                                

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

    data_sources = [nws_alerts_data, usgs_data]
    index = 0
    while index < max([(len(i.get_data_sequence)) for i in data_sources]):
        async_func_dicts = []
        serial_func_dicts = []
        for source in data_sources:
            if source.status == Status.GET_COMPLETED:
                continue
            register_dict = source.get_data_sequence[index]
            if register_dict["async"] is True:
                async_func_dicts.append(register_dict)
            else:
                serial_func_dicts.append(register_dict)
        
        asyncio.run(gather_async_register_funcs(
            usgs_data, 
            nws_alerts_data, 
            async_func_dicts, 
            triggers_usgs,
            triggers_nws_alerts
            )
        )
        run_serial_register_funcs(
            usgs_data, 
            nws_alerts_data, 
            serial_func_dicts, 
            triggers_usgs,
            triggers_nws_alerts
        )

        for source in data_sources:
            if index == len(source.get_data_sequence) - 1:
                source.status = Status.GET_COMPLETED
        
        index += 1

    index = 0
    while index < max([(len(i.filter_data_sequence)) for i in data_sources]):
        async_func_dicts = []
        serial_func_dicts = []
        for source in data_sources:
            if source.status == Status.FILTER_COMPLETED or \
                len(source.filter_data_sequence) == 0:
                continue
            register_dict = source.filter_data_sequence[index]
            if register_dict["async"] is True:
                async_func_dicts.append(register_dict)
            else:
                serial_func_dicts.append(register_dict)
        
        asyncio.run(gather_async_register_funcs(
            usgs_data, 
            nws_alerts_data, 
            async_func_dicts, 
            triggers_usgs,
            triggers_nws_alerts
            )
        )
        run_serial_register_funcs(
            usgs_data, 
            nws_alerts_data, 
            serial_func_dicts, 
            triggers_usgs,
            triggers_nws_alerts
        )

        for source in data_sources:
            if index == len(source.filter_data_sequence) - 1:
                source.status = Status.FILTER_COMPLETED

        index += 1
    
    for key, value in usgs_data.get_payload().items():
        event = events_map[key]
        if len(value) == 0:
            continue
        if event.send_message_action:
            event.send_message_action.send_message(
                utils.format_sms_earthquake(
                    event.summary,
                    value
                )
            )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()