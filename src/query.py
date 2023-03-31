import sqlite3
import sqlite3
import os 
import logging
from datetime import datetime

def get_weather_data(date=None):
    # We get all the weather data from wx_data and ingest it into the weather_data_db
    try:
        sqliteConnection = sqlite3.connect('weather_data_db.db')
        with sqliteConnection:
            cursor = sqliteConnection.cursor()
            if date is None:
                cursor.execute("SELECT * FROM weather_data")
            else:
                cursor.execute('''SELECT * FROM weather_data where date = "{}" '''.format(date))

            return cursor.fetchall()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def get_weather_data_stats(year=None):
    # We do all the transformations on top of weather data from wx_data and ingest it into the average_temp table in weather_data_db
    try:
        sqliteConnection = sqlite3.connect('weather_data_db.db')
        with sqliteConnection:
            cursor = sqliteConnection.cursor()

            if year is None:
                cursor.execute("SELECT * FROM average_temp")
            else:
                cursor.execute('''SELECT * FROM average_temp where year = "{}" '''.format(year))

            rows = cursor.fetchall()

            return rows

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

