import logging
import json
import datetime
import asyncio
import aiohttp
from .base import DataSource, Status
from .register import Register
LOGGER = logging.getLogger(__name__)

# API Reference:
# https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php

base_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"

class USGSEarthquakeData(DataSource):
    get_data_sequence = Register()
    filter_data_sequence = Register()

    def __init__(self):
        super().__init__()
        self._current_get_json = None
        self._checked_ids = []

    @get_data_sequence.add_func(index=0)
    async def get_past_hour_earthquakes(self):
        self._last_get_dt = datetime.datetime.now()
        endpoint = "all_hour.geojson"
        url = f"{base_url}{endpoint}"
        LOGGER.info(f"Getting earthquake data from url {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                self._current_get_json = await response.json()
    
    @filter_data_sequence.add_func(index=0)
    def filter_data(self, triggers):
        for trigger in triggers:
            self._current_payload[trigger.event_id] = []
        for earthquake in self._current_get_json["features"]:
            eq_id = earthquake["id"]
            LOGGER.info("Reviewing earthquake {eq_id} for filter matches.")
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
    
    def get_payload(self):
        payload = self._current_payload
        self._current_payload = {}
        return payload


