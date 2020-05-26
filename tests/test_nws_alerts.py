import pytest
import json
import asyncio
from context import nws_alerts, trigger_weather_alert

@pytest.fixture
def nws_trigger_base():
    return trigger_weather_alert.WeatherAlertTrigger(
        event_id = 'test',
        severities = ['unknown'],
        zones = None,
        location = None,
    )

def test_nws_alerts_get_data(nws_alerts_data, nws_trigger_base):
    asyncio.run(nws_alerts_data.get_alerts([nws_trigger_base], get_all=True))
    nws_alerts_data.filter_data([nws_trigger_base])
    data = nws_alerts_data.get_payload()
    assert data['test'][0]['type'] == "Feature"

def test_nws_alerts_get_keepalive(nws_alerts_data, nws_trigger_base):
    nws_trigger_base.status = "test"
    asyncio.run(nws_alerts_data.get_alerts([nws_trigger_base]))
    nws_alerts_data.filter_data([nws_trigger_base])
    keepalive_feature = nws_alerts_data.get_payload()
    keepalive_properties = keepalive_feature[nws_trigger_base.event_id][0]['properties']
    assert keepalive_properties['severity'] == "Unknown"
    assert keepalive_properties['status'] == "Test"
