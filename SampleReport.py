"""
Created on 2020/05/23

@author: kevin
"""
#!/usr/bin/python
import logging, time, configparser, os

import DBInquiry
import ExcelReport
import send_email

# Setup logger
logger = logging.getLogger()
log_file = __file__.replace(".py", ".log")
logging.basicConfig(level=logging.INFO, filename=f'{log_file}', format='%(asctime)s %(levelname)s:%(message)s')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == '__main__':


    # read config.ini
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__))+ '\config.ini')

    #FileName = "daily_draw_down.sql"
    SQLFileName = "get_name.sql"
    SQLFileName_FullPath = os.path.dirname(os.path.realpath(__file__)) + "\\" + SQLFileName
    data  = DBInquiry.run_sql_postgres(SQLFileName_FullPath)
    
    ExcelFileName = SQLFileName.replace(".sql", ".xlsx")
    ExcelFileName_FullPath = os.path.dirname(os.path.realpath(__file__)) + "\\" + ExcelFileName

    ExcelReport.write_to_excel("List of name", data, ExcelFileName_FullPath)

    '''
    send_email.send_email(email_recipient="kevin.luo@scotiabank.com", 
                          email_subject=ExcelFileName + "({business_date})", 
                          email_message="Daily Loan DrawDown Report ({business_date})", 
                          attachment_location=ExcelFileName_FullPath)
    '''