import DBInquiry
import os, sys
import pytest

def test_DBInquiry_by_string():

    column_l, data = DBInquiry.run_SQL_string ("select * from address")
    assert column_l == ['first_name', 'last_name', 'birth_year']

def test_DBInquiry_by_File():

    SQLFileName = "get_name.sql"
    SQLFileName_FullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)) , SQLFileName)
    column_l, data = DBInquiry.run_SQL_file(SQLFileName_FullPath)

    assert column_l == ['first_name', 'last_name', 'birth_year']
