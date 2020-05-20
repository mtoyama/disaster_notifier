from .trigger_earthquake import EarthquakeTrigger
from .actions import SMSMessageAction

class Event:
    def __init__(self,
                 summary=None,
                 condition=None,
                 send_message_action=None,
                 json_dict=None):
        if json_dict:
            self.summary = json_dict['summary']
            self.trigger_earthquake = EarthquakeTrigger(
                json_dict=json_dict['trigger_earthquake']
            )
            self.send_message_action = SMSMessageAction(
                json_dict=json_dict['send_message_action']
            )
        else:
            self.summary = summary
            self.condition = condition
            self.send_message_action = send_message_action