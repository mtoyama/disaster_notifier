from context import (
    actions,
    message_formatting,
    trigger_earthquake,
    trigger_weather_alert
)
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
def nws_trigger_base():
    return trigger_weather_alert.WeatherAlertTrigger(
        event_id = 'test',
        severities = ['Moderate'],
        zones = None,
        location = None,
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
    sms_messenger.send_message(
        message_formatting.format_sms_earthquake(
            "Testing!", data['test']
            )
        )

@pytest.mark.skip
def test_send_message_nws_alerts(sms_messenger,
                                 nws_alerts_data,
                                 nws_trigger_base,
                                 test_nws_alerts_json_dict):
    nws_alerts_data._current_get_json = test_nws_alerts_json_dict
    nws_alerts_data.filter_data([nws_trigger_base])    
    data = nws_alerts_data.get_payload()
    sms_messenger.send_message(
        message_formatting.format_sms_nws_alert(
            "Testing!", data['test']
            )
        )