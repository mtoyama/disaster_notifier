import pytest
import json
from context import TEST_CONFIG_JSON, TEST_USGS_JSON
from context import usgs

@pytest.fixture
def test_config_json_dict():
    with open(TEST_CONFIG_JSON, 'r') as json_file:
        return json.load(json_file)

@pytest.fixture
def test_usgs_json_dict():
    with open(TEST_USGS_JSON, 'r') as json_file:
        return json.load(json_file)

@pytest.fixture
def user(test_config_json_dict):
    test_user = user.User(json_dict=test_config_json_dict["users"][0])

@pytest.fixture
def usgs_data():
    return usgs.USGSEarthquakeData()