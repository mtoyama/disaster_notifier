import pytest
import json
from context import TEST_CONFIG_JSON, TEST_USGS_JSON, TEST_NWS_ALERTS_JSON
from context import usgs, nws_alerts

@pytest.fixture
def test_config_json_dict():
    with open(TEST_CONFIG_JSON, 'r') as json_file:
        return json.load(json_file)

@pytest.fixture
def test_usgs_json_dict():
    with open(TEST_USGS_JSON, 'r') as json_file:
        return json.load(json_file)

@pytest.fixture
def test_nws_alerts_json_dict():
    with open(TEST_NWS_ALERTS_JSON, 'r') as json_file:
        return json.load(json_file)

@pytest.fixture
def user(test_config_json_dict):
    test_user = user.User(json_dict=test_config_json_dict["users"][0])

@pytest.fixture
def usgs_data():
    return usgs.USGSEarthquakeData()

@pytest.fixture
def nws_alerts_data():
    return nws_alerts.NWSAlertsData()