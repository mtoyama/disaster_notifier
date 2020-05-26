import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
print(sys.path)

from src.config import user, trigger_earthquake, trigger_weather_alert, actions
from src.data_sources import usgs, nws_alerts, register
from src import utils, monitors, message_formatting

data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
TEST_CONFIG_JSON = os.path.join(data_folder, 'test_config.json')
TEST_USGS_JSON = os.path.join(data_folder, 'test_usgs.json')
TEST_NWS_ALERTS_JSON = os.path.join(data_folder, 'test_nws_alerts.json')