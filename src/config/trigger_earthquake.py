import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from src import utils

class EarthquakeTrigger:
    def __init__(self,
                 json_dict=None,
                 event_id=None,
                 min_magnitude=None,
                 tsunami=None,
                 location=None,
                 radius=None):
        self.event_id = event_id
        if json_dict:
            self.min_magnitude = json_dict['min_magnitude']
            self.tsunami = json_dict['tsunami']
            self.location = json_dict['location']
            self.radius = json_dict['radius']
        else:
            self.min_magnitude = min_magnitude
            self.tsunami = tsunami
            self.location = location
            self.radius = radius
    
    def test_trigger(self,
                     magnitude,
                     tsunami,
                     location):
        array = [
            self.test_min_magnitude(magnitude),
            self.test_tsunami(tsunami),
            self.test_location(location)
        ]

        if False in array:
            return False
        else:
            return True

    def test_min_magnitude(self, magnitude):
        if self.min_magnitude is None: 
            return True
        elif magnitude >= self.min_magnitude:
            return True
        else:
            return False
    
    def test_tsunami(self, tsunami):
        if self.tsunami is None:
            return True
        elif tsunami == self.tsunami:
            return True
        else:
            return False
    
    def test_location(self, location):
        if self.location is None or self.radius is None:
            return True

        distance = utils.lat_long_check_within_radius(location, self.location)
        if distance <= self.radius:
            return True
        else:
            return False

