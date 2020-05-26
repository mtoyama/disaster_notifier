import logging
import json
import datetime
import asyncio
import aiohttp
from .base import DataSource, Status
from .register import register_source_action
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from src import timing
LOGGER = logging.getLogger(__name__)

# API Reference:
# https://www.weather.gov/documentation/services-web-api#/default/get_alerts_active

base_url = "https://api.weather.gov/alerts/active"
# Unclear how often this is updated, but let's try to get most up-to-date alerts.
get_interval_s = 60 

class NWSAlertsData(DataSource):
    def __init__(self):
        super().__init__()
        self._checked_ids = []
        self._current_get_json = None

    @register_source_action
    async def get_alerts(self, triggers, get_all=False):
        self._current_get_json = None
        duration = datetime.datetime.now() - self._last_get_dt
        if duration.total_seconds() < get_interval_s:
            LOGGER.info(f"Get interval not elapsed -- skipping get.")
            return False

        for trigger in triggers:
            self._current_payload[trigger.event_id] = []
        for trigger in triggers:
            url = f"{base_url}"
            params = None
            if get_all is False:
                params = {
                    "status": trigger.status,
                    "message_type": trigger.message_type,
                }
                if trigger.zones:
                    params['zone'] = ",".join(trigger.zones)
                if trigger.severities:
                    params['severity'] = ",".join(trigger.severities)
                if trigger.location:
                    params['location'] = ",".join(trigger.location)
            LOGGER.info(f"Getting weather alert data from url {url}, {params}")
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                     self._current_get_json = await response.json()
            LOGGER.info(f"Weather alert data get complete from {url}, {params}")
            self._last_get_dt = datetime.datetime.now()
            self.status = Status.GET_COMPLETED
            return True

    @register_source_action
    def filter_data(self, triggers) -> bool:
        if not self._current_get_json:
            LOGGER.info("No data available for filtering -- skipping filter step")
            return False
        for trigger in triggers:
            self._current_payload[trigger.event_id] = []
        for alert in self._current_get_json['features']:
            alert_id = alert['properties']['id']
            for trigger in triggers:
                LOGGER.info(f"Checking alert {alert_id} for id matches")
                if alert_id not in self._checked_ids:
                    self._current_payload[trigger.event_id].append(alert)
            self._checked_ids.append(alert_id)
        self.status = Status.FILTER_COMPLETED
        return True