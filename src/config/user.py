import json
from .event import Event

class User:
    def __init__(self,
                 id=id,
                 name=None,
                 phone_number=None,
                 events=None,
                 json_dict=None):
        if json_dict:
            self.id = json_dict['id']
            self.name = json_dict['name']
            self.phone_number = json_dict['phone_number']
            self.events = [Event(json_dict=event_dict) for event_dict in json_dict['events']]
        else:
            self.id = id
            self.name = name
            self.phone_number = phone_number
            self.events = events