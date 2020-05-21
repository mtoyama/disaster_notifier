import json
import pytest
from context import user

def test_basic_initialization(test_config_json_dict):
    test_user = user.User(json_dict=test_config_json_dict["users"][0])
    assert test_user.id == "54d4af26-0195-46f7-8a9c-1bf3c43acf90"
    assert test_user.name == "Mike T"
    assert test_user.phone_number_key == "MIKE_PHONE"
    test_event = test_user.events[0]
    assert test_event.summary == "Earthquake: Magnitude 7.0+"
    assert test_event.trigger_earthquake.id == "f615814a-71d9-407a-800d-f213c5bef56a"
    assert test_event.trigger_earthquake.min_magnitude == 7
    assert test_event.trigger_earthquake.tsunami == None
    assert test_event.trigger_earthquake.location == None
    assert test_event.trigger_earthquake.radius == None
    assert test_event.send_message_action.phone_number_key == "MIKE_PHONE"