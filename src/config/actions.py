from twilio.rest import Client
import os

class SMSMessageAction:
    def __init__(self, phone_number_key=None, json_dict=None):
        if json_dict:
            self.phone_number_key = json_dict['phone_number_key']
        else:
            self.phone_number_key = phone_number_key
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    def send_message(self, message):
        client = Client(
            account_sid=self.account_sid,
            password=self.auth_token)
        message = client.messages.create(
            body=message,
            from_='+12029339696',
            to=os.getenv(self.phone_number_key)
        )