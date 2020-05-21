from twilio.rest import Client

class SMSMessageAction:
    def __init__(self, phone_number=None, json_dict=None):
        if json_dict:
            self.phone_number = json_dict['phone_number']
        else:
            self.phone_number = phone_number

    def send_message(self, message):
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message,
            from_='+12029339696',
            to=self.phone_number
        )