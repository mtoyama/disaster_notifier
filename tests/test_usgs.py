import pytest
import json
import asyncio
from context import usgs, trigger_earthquake, TEST_USGS_JSON

@pytest.fixture
def earthquake_trigger_base():
    return trigger_earthquake.EarthquakeTrigger(
        id = 'test',
        min_magnitude = 0,
        tsunami = None,
        location = None,
        radius = None,
    )

def test_usgs_filter_mock(usgs_data,
                          earthquake_trigger_base,
                          test_usgs_json_dict):
    usgs_data._current_get_json = test_usgs_json_dict
    usgs_data.filter_data([earthquake_trigger_base])
    assert len(usgs_data.get_payload()['test']) == 8

    usgs_data.filter_data([earthquake_trigger_base])
    # All of the earthquake IDs in the previous payload should be registered.
    # When we run the fiter again, all of the previous payload's earthquakes
    # should be filtered from being added to the next payload.
    assert len(usgs_data.get_payload()['test']) == 0

def test_usgs_get_data(usgs_data):
    asyncio.run(usgs_data.get_past_hour_earthquakes())
    data = usgs_data._current_get_json
    assert data['type'] == "FeatureCollection"