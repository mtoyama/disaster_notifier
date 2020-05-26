from twilio.rest import Client
import os
import functools
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from src import monitors

FROM_NUMBER = os.getenv('FROM_NUMBER')
RATE_LIMITER = monitors.RateLimiter(limit_frame=60, limit_count=10)

class SMSMessageAction:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    def __init__(self, phone_number_key=None, json_dict=None):
        if json_dict:
            self.phone_number_key = json_dict['phone_number_key']
        else:
            self.phone_number_key = phone_number_key

    @RATE_LIMITER.limit_call_rate
    def send_message(self, message):
        client = Client(
            account_sid=self.__class__.account_sid,
            password=self.__class__.auth_token)
        message = client.messages.create(
            body=message,
            from_=FROM_NUMBER,
            to=os.getenv(self.phone_number_key)
        )