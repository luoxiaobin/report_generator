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

def RunSQLString(strSQL):

    # read config.ini
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database.ini'))

    database = config.get('General', 'database')

    conn = None
    if (database == 'SQLite'):
        SQLiteDBFile = config.get('SQLite', 'db_file_name')
        logger.debug(f"SQLite_db={os.path.dirname(os.path.realpath(__file__))+ '//' + SQLiteDBFile}")
        conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)), SQLiteDBFile))
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

        ColList = []
        for i in range(len(columns_descr)):
            ColList.append(columns_descr[i][0])

        data =[]
        RecordCount = 0
        for row in rows:
            RecordCount = RecordCount + 1
            data.append(row)

        logger.info(f"Total {RecordCount} records processed")

        cur.close()
        conn.close()
        logger.debug("Database connection closed")
        return (ColList, data)


    except (Exception, psycopg2.DatabaseError):
        logger.warning("Something wrong in performing SQL query:")
        return ("","")

def RunSQLFile(SQLFile):

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

    return RunSQLString(strSQL)


if __name__ == '__main__':

    SQLFileName = "get_name.sql"
    SQLFileName_FullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)) , SQLFileName)
    #column_l, data = run_sql_postgres(SQLFileName_FullPath)

    column_l, data = RunSQLFile(SQLFileName_FullPath)
    print (column_l)
    print(data)
    
    column_l, data = RunSQLString ("select * from address")
    logger.info (column_l)

    print (column_l)
    print(data)
    
    
   
