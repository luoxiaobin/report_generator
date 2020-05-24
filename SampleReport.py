"""
Created on 2020/05/23

@author: Kevin Luo
"""
#!/usr/bin/python
import logging, time, configparser, os

#custom library
import DBInquiry
import ExcelReport
import send_email

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

log_file = __file__.replace(".py", ".log")
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)

#logging.basicConfig(level=logging.INFO, filename=f'{log_file}', format='%(asctime)s %(levelname)s:%(message)s')
sh = logging.StreamHandler()
sh.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

fh.setFormatter(formatter)
sh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(sh)


if __name__ == '__main__':

    logger.info(f"Program {__file__} started:")
    # read config.ini
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__))+ '\\config.ini')

    #FileName = "daily_draw_down.sql"
    SQLFileName = "film.sql"
    SQLFileName_FullPath = os.path.dirname(os.path.realpath(__file__)) + "\\" + SQLFileName
    column, data  = DBInquiry.run_sql_postgres(SQLFileName_FullPath)
    
    ExcelFileName = SQLFileName.replace(".sql", ".xlsx")
    ExcelFileName_FullPath = os.path.dirname(os.path.realpath(__file__)) + "\\" + ExcelFileName


    logger.info(column)
    ExcelReport.write_to_excel(report_name="Name List", column=column, data=data, file_name=ExcelFileName_FullPath)

    '''
    send_email.send_email(receiver_email="kevin.xiaobin.luo@gmail.com", 
                          email_subject=ExcelFileName , 
                          email_message="Test Message", 
                          attachment_location=ExcelFileName_FullPath)
    '''