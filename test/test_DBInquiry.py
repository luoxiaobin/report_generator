import DBInquiry
import os, sys
import pytest

def test_DBInquiry_by_string():

    column_l, data = DBInquiry.run_sql_string ("select * from address")
    assert column_l == ['first_name', 'last_name', 'birth_year']

def test_DBInquiry_by_File():

    sql_filename_fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)) , "test.sql")

    if os.path.isfile(sql_filename_fullpath):
        os.remove(sql_filename_fullpath)

    with open(sql_filename_fullpath, "w") as sql_test_file:
        sql_test_file.write("select * from address")

    column_l, data = DBInquiry.run_sql_file(sql_filename_fullpath)

    assert column_l == ['first_name', 'last_name', 'birth_year']
