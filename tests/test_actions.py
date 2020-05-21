from context import actions
import pytest

@pytest.fixture
def sms_messenger():
    return actions.SMSMessageAction(phone_number_key="MIKE_PHONE")

@pytest.mark.skip
def test_send_message(sms_messenger):
    sms_messenger.send_message("Testing!")