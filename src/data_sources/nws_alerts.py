import logging
import json
import datetime
import asyncio
import aiohttp
from .base import DataSource, Status
from .register import Register
LOGGER = logging.getLogger(__name__)

# API Reference:
# https://www.weather.gov/documentation/services-web-api#/default/get_alerts_active

base_url = "https://api.weather.gov/alerts/active"

class USGSEarthquakeData(DataSource):
    get_data_sequence = Register()
    filter_data_sequence = Register()

    def __init__(self):
        super.__init__()

    @get_data_sequence.add_func(index=0)
    async def get_alerts(self, triggers):
        self._last_get_dt = datetime.datetime.now()
        for trigger in triggers:
            self._current_payload[trigger.id] = []
        for trigger in triggers:    
            url = f"{base_url}"
            url += "?"
            url += f"status={trigger.status}"
            url += f"message_type={trigger.message_type}"
            url += f"zone={','.join(trigger.zones)}"
            url += f"severity={','.join(trigger.severities)}"

            LOGGER.info(f"Getting weather alert data from url {url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    self._current_payload[trigger.event_id] = \
                        await response.json()["features"]