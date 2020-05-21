from context import actions
import pytest

@pytest.fixture
def sms_messenger():
    return actions.SMSMessageAction(phone_number="+18084895996")

@pytest.mark.skip
def test_send_message(sms_messenger):
    sms_messenger.send_message("Testing!")