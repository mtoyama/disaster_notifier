from context import trigger_earthquake
import pytest

@pytest.fixture
def earthquake_trigger():
    return trigger_earthquake.EarthquakeTrigger(
        id = 'test',
        min_magnitude = 5,
        tsunami = 0,
        location = None, #TBI
        radius = None, #TBI
    )

@pytest.mark.parametrize("min_mag_override,input,expected", [
    (5, 1, False), (5, 5, True), (5, 7, True), (None, 0, True)
    ])
def test_min_magnitude(earthquake_trigger, min_mag_override, input, expected):
    earthquake_trigger.min_magnitude = min_mag_override
    assert earthquake_trigger.test_min_magnitude(input) == expected

@pytest.mark.parametrize("tsunami_override, input,expected", [
    (0, 1, False), (0, 0, True), (None, 0, True)])
def test_tsunami(earthquake_trigger, tsunami_override, input, expected):
    earthquake_trigger.tsunami = tsunami_override
    assert earthquake_trigger.test_tsunami(input) == expected