import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from src import utils

class WeatherAlertTrigger:
    def __init__(self,
                 json_dict=None,
                 event_id=None,
                 severities=None,
                 zones=None,
                 location=None):
        self.event_id = event_id
        if json_dict:
            self.severities = json_dict['severities']
            self.zones = json_dict['zones']
            self.location = json_dict['location']
        else:
            self.severities = severities
            self.zones = zones
            self.location = location
        
        # Hard coded query values
        self.status = "actual"
        self.message_type = "alert"
