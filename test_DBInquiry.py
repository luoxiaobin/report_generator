import DBInquiry
import os, sys
import pytest

def TestDBInquirybyString():

    column_l, data = DBInquiry.RunSQLString ("select * from address")
    assert column_l == ['first_name', 'last_name', 'birth_year']

def TestDBInquiryByFile():

    SQLFileName = "get_name.sql"
    SQLFileName_FullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)) , SQLFileName)
    column_l, data = DBInquiry.RunSQLFile(SQLFileName_FullPath)

    assert column_l == ['first_name', 'last_name', 'birth_year']
