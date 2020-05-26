from context import register
import logging
LOGGER = logging.getLogger(__name__)

def test_register(usgs_data, nws_alerts_data):
    assert len(register.register_source_action.actions) == 4
    function = register.SourceRegister.get_source_action_at_index(
        usgs_data.__class__, 0
    )
    assert function.__name__ == 'get_past_hour_earthquakes'