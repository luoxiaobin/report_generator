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

def run_sql_SQLite(SQLFile, SQLite_db_file):
    
    # read config.ini
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__))+ '//' +'database.ini')

    if not os.path.isfile(SQLFile):
        logger.error(f"SQL file {SQLFile} doesn't exist!")
        return "Error", ""

    logger.info(f"Read SQL file {SQLFile}...")    
    f=open(SQLFile,'r')
    strSQL = f.read()
    f.close()
    
    column = []
    data =[]
    conn = None

    try:
        #conn = psycopg2.connect(**db)
        conn = sqlite3.connect(SQLite_db_file)
        logger.debug(f"SQLite_db={SQLite_db_file}")

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
            col_l.append(columns_descr[i])

        #data.append(col_l)

        count = 0
        for row in rows:
            count = count + 1
            data.append(row)

        logger.info(f"Total {count} records processed")

        cur.close()
        conn.close()
        logger.debug("Database connection closed")
        return (col_l, data)


    except (Exception, psycopg2.DatabaseError):
        logger.warning("Something wrong in performing SQL query:")
        return ("","")

def run_sql_postgres(SQLFile):
    
    IniFile = 'database.ini'
    if not os.path.isfile(IniFile):
        logger.error(f"Ini file {IniFile} doesn't exist!")
        return "Error, "

    # read config.ini
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__))+ '//' +'database.ini')

    # get section, default to postgresql
    host = config.get('postgresql', 'host')
    port = config.get('postgresql', 'port')
    database = config.get('postgresql', 'database')
    dbuser = config.get('postgresql', 'user')
    password = config.get('postgresql', 'password')

    if not os.path.isfile(SQLFile):
        logger.error(f"SQL file {SQLFile} doesn't exist!")
        return "Error"

    logger.info(f"Read SQL file {SQLFile}...")    
    f=open(SQLFile,'r')
    strSQL = f.read()
    f.close()
    
    column = []
    data =[]
    conn = None

    try:
        #conn = psycopg2.connect(**db)
        conn = psycopg2.connect(f"host={host} port={port} dbname={database} user={dbuser} password={password}")
        logger.debug(f"host={host} port={port} dbname={database} user={dbuser}")


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
            col_l.append(columns_descr[i])

        #data.append(col_l)

        count = 0
        for row in rows:
            count = count + 1
            data.append(row)

        logger.info(f"Total {count} records processed")

        cur.close()
        conn.close()
        logger.debug("Database connection closed")
        return (col_l, data)


    except (Exception, psycopg2.DatabaseError):
        logger.warning("Something wrong in performing SQL query:")


if __name__ == '__main__':

    SQLFileName = "get_name.sql"
    SQLFileName_FullPath = os.path.dirname(os.path.realpath(__file__)) + "\\" + SQLFileName
    #column_l, data = run_sql_postgres(SQLFileName_FullPath)

    column_l, data = run_sql_SQLite(SQLFileName, os.path.dirname(os.path.realpath(__file__)) + "\\test.db")
    
    logger.info (column_l)

    print (column_l)
    print(data)
    
    
   
