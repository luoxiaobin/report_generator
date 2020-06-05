import DBInquiry
import os, sys
import pytest

def test_DBInquiry_by_string():

    column_l, data = DBInquiry.run_sql_string ("select * from address")
    assert column_l == ['first_name', 'last_name', 'birth_year']

def test_DBInquiry_by_File():

    sql_file_name = "get_name.sql"
    sql_filename_fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)) , sql_file_name)
    column_l, data = DBInquiry.run_sql_file(sql_filename_fullpath)

    assert column_l == ['first_name', 'last_name', 'birth_year']
