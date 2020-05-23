from .trigger_earthquake import EarthquakeTrigger
from .trigger_weather_alert import WeatherAlertTrigger
from .actions import SMSMessageAction
import uuid

class Event:
    def __init__(self,
                 summary=None,
                 trigger=None,
                 send_message_action=None,
                 json_dict=None):
        self.id = uuid.uuid4().hex
        if json_dict:
            self.summary = json_dict['summary']
            if json_dict['trigger']['type'] =='earthquake':
                self.trigger = EarthquakeTrigger(
                    event_id=self.id,
                    json_dict=json_dict['trigger']
                )
            if json_dict['trigger']['type'] =='weather_alert':
                self.trigger = WeatherAlertTrigger(
                    event_id=self.id,
                    json_dict=json_dict['trigger']
                )
            self.send_message_action = SMSMessageAction(
                json_dict=json_dict['send_message_action']
            )
        else:
            self.summary = summary
            self.trigger = trigger
            self.trigger.event_id = self.id
            self.send_message_action = send_message_action