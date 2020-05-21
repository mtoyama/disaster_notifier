from context import actions, utils, trigger_earthquake
import pytest

@pytest.fixture
def earthquake_trigger_base():
    return trigger_earthquake.EarthquakeTrigger(
        id = 'test',
        min_magnitude = 3.1,
        tsunami = None,
        location = None, #TBI
        radius = None, #TBI
    )

@pytest.fixture
def sms_messenger():
    return actions.SMSMessageAction(phone_number_key="MIKE_PHONE")

@pytest.mark.skip
def test_send_message(sms_messenger):
    sms_messenger.send_message("Testing!")

@pytest.mark.skip
def test_send_message_eq_info(sms_messenger,
                              usgs_data,
                              earthquake_trigger_base,
                              test_usgs_json_dict):
    usgs_data._current_get_json = test_usgs_json_dict
    usgs_data.filter_data([earthquake_trigger_base])    
    data = usgs_data.get_payload()
    sms_messenger.send_message(utils.format_sms_earthquake("Testing!", data['test']))