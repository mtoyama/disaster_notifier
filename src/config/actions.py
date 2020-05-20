from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACb028947829ceec6bf59df837848bcbc0'
auth_token = '1ee987a6bd4cf4f4bc9d720bf3fb5c41'

class SMSMessageAction:
    def __init__(self, phone_number, json_dict=None):
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