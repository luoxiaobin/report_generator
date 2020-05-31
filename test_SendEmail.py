import SendEmail
import os
import pytest

def TestSendEmail():

    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "get_name.sql")
    if (SendEmail.send_email("abc@gmail.com", "test", "body message", file) != True):
        pytest.fail("Failed in email")
    else:
        pass


    

