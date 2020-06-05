# Brief intro

* The idea is to solution an easy excel report generator by using Python toolset
* It contains the following modules:
  * _DBInquiry.py_: to read data from database (SQLite/Postgres)
  * _ExcelReport.py_: based on provided data (list), will create excel and do basic formatting
  * _SendEmail_: send email with the report as attachment

* GitHub action has been enabled for automatic CI (each commit will trigger a Python app build and run Pytest)
