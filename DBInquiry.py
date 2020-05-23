"""
Created on 2020/05/23

@author: kevin
"""

#!/usr/bin/python
import psycopg2
from configparser import ConfigParser

import logging, time, configparser, os

# Setup logger
logger = logging.getLogger(__name__)

# read config.ini
config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__))+ '//' +'database.ini')

def run_sql_postgres(strFileName):
    try:
        
        # create a parser
        parser = ConfigParser()
        
        filename = 'database.ini'
        section='postgresql'
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))


        logger.info(f"Start processing SQL file {strFileName}...")    
        f=open(strFileName,'r')
        strSQL = f.read()
        f.close()
    except FileNotFoundError:
        logger.warning(f"File '{strFileName}' doesn't exist!")

    data =[]
    conn = None

    try:

        conn = psycopg2.connect(**db)
        logger.debug(f'Connecting tod database: {conn}, with parameter {db}')

        cur = conn.cursor()
        cur.execute(strSQL)

        logger.info(f"The number of actors: {cur.rowcount}")


        columns_descr = cur.description
        rows = cur.fetchall()

        for row in rows:
            # print(row)
            row = cur.fetchone()

        col_l = []
        for i in range(len(columns_descr)):
            col_l.append(columns_descr[i][0])

        data.append(col_l)

        count = 0
        for row in rows:
            count = count + 1
            data.append(row)

        logger.info(f"Total {count} records processed")

        cur.close()
        conn.close()
        logger.debug("Database connection closed")
        return (data)


    except (Exception, psycopg2.DatabaseError) as error:
        logger.warning("Something wrong in performing SQL query:")
        logger(error)


if __name__ == '__main__':

    logger.info(__name__)
    SQLFileName = "test.sql"
    SQLFileName_FullPath = os.path.dirname(os.path.realpath(__file__)) + "\\" + SQLFileName
    data = run_sql_postgres(SQLFileName_FullPath)

    logger.info(data)
    
