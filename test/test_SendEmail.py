import SendEmail
import os
import pytest

def test_send_email():

    sql_filename_fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)) , "test.sql")

    if os.path.isfile(sql_filename_fullpath):
        os.remove(sql_filename_fullpath)

    with open(sql_filename_fullpath, "w") as sql_test_file:
        sql_test_file.write("select * from address")

    
    if (SendEmail.send_email("abc@gmail.com", "test", "body message", sql_filename_fullpath) != True):
       pass
    

    

