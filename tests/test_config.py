import json
import pytest
from .context import src.config
from .context import (
    TEST_CONFIG_JSON,
    TEST_USGS_JSON
)

def test_basic_initialization():
    data = json.load(TEST_CONFIG_JSON)
    test_user = src.config.user.User(json_dict=data["users"][0])
    print(test_user)