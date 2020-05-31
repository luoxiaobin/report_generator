import DBInquiry
import os, sys
import pytest

def test_DBInquiry_string():

    column_l, data = DBInquiry.run_sqlString ("select * from address")
    assert column_l == ['first_name', 'last_name', 'birth_year']

def test_DBInquiry_file():

    SQLFileName = "get_name.sql"
    SQLFileName_FullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)) , SQLFileName)
    column_l, data = DBInquiry.run_sql(SQLFileName_FullPath)

    assert column_l == ['first_name', 'last_name', 'birth_year']
