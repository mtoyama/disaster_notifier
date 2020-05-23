import logging
import json
import datetime
import asyncio
import aiohttp
from .base import DataSource, Status
LOGGER = logging.getLogger(__name__)

# API Reference:
# https://www.weather.gov/documentation/services-web-api#/default/get_alerts_active

base_url = "https://api.weather.gov/alerts/active"

class NWSAlertsData(DataSource):
    filter_data_sequence = []

    def __init__(self):
        super().__init__()
        self.get_data_sequence = []
        self.add_method_to_register(
            self.get_alerts,
            self.get_data_sequence,
            0
            )

    async def get_alerts(self, triggers, get_all=False):
        self._last_get_dt = datetime.datetime.now()
        for trigger in triggers:
            self._current_payload[trigger.event_id] = []
        for trigger in triggers:
            url = f"{base_url}"
            if get_all is False:
                url += "?"
                queries = [
                    f"status={trigger.status}",
                    f"message_type={trigger.message_type}",
                ]
                if trigger.zones:
                    queries.append(f"zone={','.join(trigger.zones)}")
                if trigger.severities:
                    queries.append(f"severity={','.join(trigger.severities)}")
                if trigger.location:
                    queries.append(f"location={','.join(trigger.location)}")
                url += "&".join(queries)

            LOGGER.info(f"Getting weather alert data from url {url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    self._current_payload[trigger.event_id] = data['features']