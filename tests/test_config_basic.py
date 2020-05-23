import json
import pytest
from context import user

def test_basic_initialization(test_config_json_dict):
    test_user = user.User(json_dict=test_config_json_dict["users"][0])
    assert test_user.id == "54d4af26-0195-46f7-8a9c-1bf3c43acf90"
    assert test_user.name == "Mike T"
    assert test_user.phone_number_key == "MIKE_PHONE"
    test_event = test_user.events[0]
    assert test_event.summary == "Earthquake: Magnitude 6.0+"
    assert test_event.trigger.min_magnitude == 6
    assert test_event.trigger.tsunami == None
    assert test_event.trigger.location == None
    assert test_event.trigger.radius == None
    assert test_event.send_message_action.phone_number_key == "MIKE_PHONE"