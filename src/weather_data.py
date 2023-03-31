import sqlite3
import os 
import logging
from datetime import datetime

def task():
    try:
        sqliteConnection = sqlite3.connect('weather_data_db.db')
        with sqliteConnection:
            cursor = sqliteConnection.cursor()
            print("Database created and Successfully Connected to SQLite and Loading Data ...")
            logging.basicConfig(filename="/Users/kaluvavenkateswarlu/Documents/Insightary/coding_test/code-challenge-template-main/answers/log_times.log", level=logging.INFO, filemode="w")


            # Dropping the existing older table if it exists
            sqlite_delete_table_query = '''drop TABLE if exists weather_data ;'''
            cursor.execute(sqlite_delete_table_query)

            sqlite_create_table_query = '''CREATE TABLE if not exists weather_data (
                                            date DATE NOT NULL,
                                            max_temp NUMERIC NOT NULL,
                                            min_temp NUMERIC NOT NULL,
                                            precipitation NUMERIC NOT NULL
                                        );'''

            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()

            # Fetching all records from txt files and inserting the raw data into weather_data table

            dir_list = os.listdir('/Users/kaluvavenkateswarlu/Documents/Insightary/coding_test/code-challenge-template-main/wx_data/')
            for path in dir_list:
                logging.info(path+" start time: "+ str(datetime.now()))
                with open("/Users/kaluvavenkateswarlu/Documents/Insightary/coding_test/code-challenge-template-main/wx_data/"+path) as file:
                    line_count=0
                    for item in file:
                        date,maxtemp,mintemp,prec = item.strip().split("\t")
                        cursor.execute("INSERT INTO weather_data VALUES ({},{},{},{})".format(date,maxtemp,mintemp,prec))
                        line_count+=1
                logging.info(path+" end time: "+str(datetime.now()))
                logging.info(path+"- number of records ingested: " + str(line_count))

            sqliteConnection.commit()

            # this statement will make sure we do not have any duplicate records
            delete_duplicate = '''DELETE FROM weather_data
                                WHERE rowid NOT IN (
                                SELECT MIN(rowid) 
                                FROM weather_data 
                                GROUP BY date,max_temp,min_temp,precipitation
                                )'''
            cursor.execute(delete_duplicate)
            
            sqliteConnection.commit()

            # intermediate table for stats that are required
            sqlite_delete_table_query = '''drop TABLE if exists average_temp ;'''
            cursor.execute(sqlite_delete_table_query)
            sqliteConnection.commit()
            print("SQLite table created")

            # Calculating the statistics on temperatures and precipitation and storing it in the average_temp intermediate table
            min_max_model = ''' CREATE TABLE average_temp as 
                            SELECT substr(date,1,4) as year, AVG(max_temp) as avg_max_temp, AVG(min_temp) as avg_min_temp, SUM(precipitation) as total_accumulated_precipitation 
                                FROM weather_data where min_temp != -9999 and max_temp!= -9999 group by year
                                '''
            cursor.execute(min_max_model)
            sqliteConnection.commit()

            cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
