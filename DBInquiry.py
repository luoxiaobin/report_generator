"""
Created on 2020/05/23

@author: kevin
"""

#!/usr/bin/python
import psycopg2
from configparser import ConfigParser
import logging, time, configparser, os
import sqlite3

# Setup logger
logger = logging.getLogger(__name__)

def run_sqlString(strSQL):

    # read config.ini
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database.ini'))

    database = config.get('General', 'database')

    conn = None
    if (database == 'SQLite'):
        SQLite_db_file = config.get('SQLite', 'db_file_name')
        logger.debug(f"SQLite_db={os.path.dirname(os.path.realpath(__file__))+ '//' + SQLite_db_file}")
        conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__))+ '//' + SQLite_db_file)
    elif (database == 'postgres'):
        # get section, default to postgresql
        host = config.get('postgresql', 'host')
        port = config.get('postgresql', 'port')
        database = config.get('postgresql', 'database')
        dbuser = config.get('postgresql', 'user')
        password = config.get('postgresql', 'password')
        logger.debug(f"Connecting postgres host={host} port={port} dbname={database} user={dbuser} password=???")
        conn = psycopg2.connect(f"host={host} port={port} dbname={database} user={dbuser} password={password}")
    else:
        logger.error("Can`t find database in ini file")
        return "Error", ""

    # below code is generic for various database
    try:

        cur = conn.cursor()
        cur.execute(strSQL)

        logger.info(f"The number of records: {cur.rowcount}")

        columns_descr = cur.description
        rows = cur.fetchall()

        for row in rows:
            row = cur.fetchone()

        col_l = []
        for i in range(len(columns_descr)):
            col_l.append(columns_descr[i][0])

        data =[]
        rec_count = 0
        for row in rows:
            rec_count = rec_count + 1
            data.append(row)

        logger.info(f"Total {rec_count} records processed")

        cur.close()
        conn.close()
        logger.debug("Database connection closed")
        return (col_l, data)


    except (Exception, psycopg2.DatabaseError):
        logger.warning("Something wrong in performing SQL query:")
        return ("","")

def run_sql(SQLFile):

    if not os.path.isfile(SQLFile):
        logger.error(f"SQL file {SQLFile} doesn't exist!")
        return "Error", ""

    try:
        f=open(SQLFile,'r')
        strSQL = f.read()
        f.close()
    except (Exception):
        logger.warning(f"Can't read from {SQLFile}")
        return ("","")

    return run_sqlString(strSQL)


if __name__ == '__main__':

    SQLFileName = "get_name.sql"
    SQLFileName_FullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)) , SQLFileName)
    #column_l, data = run_sql_postgres(SQLFileName_FullPath)

    column_l, data = run_sql(SQLFileName_FullPath)
    print (column_l)
    print(data)
    
    column_l, data = run_sqlString ("select * from address")
    logger.info (column_l)

    print (column_l)
    print(data)
    
    
   
