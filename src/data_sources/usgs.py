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
# https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php

base_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"
# all_hour.geojson updated every 60s, and it is important to get very recent
# earthquake data.
get_interval_s = 60 

class USGSEarthquakeData(DataSource):
    def __init__(self):
        super().__init__()
        self._current_get_json = None

    @register_source_action
    async def get_past_hour_earthquakes(self):
        self._current_get_json = None
        duration = datetime.datetime.now() - self._last_get_dt
        if duration.total_seconds() < get_interval_s:
            LOGGER.info(f"Get interval not elapsed -- skipping get.")
            return False
        endpoint = "all_hour.geojson"
        url = f"{base_url}{endpoint}"
        LOGGER.info(f"Getting earthquake data from url {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                self._current_get_json = await response.json()
        LOGGER.info(f"Earthquake data get complete for url {url}")
        self._last_get_dt = datetime.datetime.now()
        self.status = Status.GET_COMPLETED
        return True

    @register_source_action
    def filter_data(self, triggers) -> bool:
        if not self._current_get_json:
            LOGGER.info("No data available for filtering -- skipping filter.")
            return False
        for trigger in triggers:
            self._current_payload[trigger.event_id] = []
        LOGGER.debug(f"Filter list: {self._checked_ids}")
        for earthquake in self._current_get_json["features"]:
            eq_id = earthquake["id"]
            LOGGER.info(f"Reviewing earthquake {eq_id} for filter matches.")
            if eq_id in self._checked_ids:
                LOGGER.info(f"Earthquake already reviewed -- skipping.")
                continue
            for trigger in triggers:
                # Reverse the tuple to be latitude first
                location = (earthquake["geometry"]["coordinates"][1],
                            earthquake["geometry"]["coordinates"][0])
                if trigger.test_trigger(
                    earthquake["properties"]["mag"],
                    earthquake["properties"]["tsunami"],
                    location) is True:
                    self._current_payload[trigger.event_id].append(earthquake)
            self._checked_ids.append(eq_id)
        self.status = Status.FILTER_COMPLETED
        return True