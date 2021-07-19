import mysql.connector
import csv

import db_config
from process_working_hours import process_working_hours

# Define the table names
REST_TABLE_NAME = "restaurants_table"
DAY_TABLE_NAME = "restaurants_on_day_table"

# This function drops the table if exists and create the tables to load data again
def drop_existing_table_and_create(cursor):
    rest_table_drop_command = "DROP TABLE IF EXISTS " + REST_TABLE_NAME
    cursor.execute(rest_table_drop_command)

    day_table_drop_command = "DROP TABLE IF EXISTS " + DAY_TABLE_NAME
    cursor.execute(day_table_drop_command)

    rest_table_create_command = "CREATE TABLE " + REST_TABLE_NAME + \
        " (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(1000))"
    cursor.execute(rest_table_create_command)

    day_table_create_command = "CREATE TABLE " + DAY_TABLE_NAME + \
        "(id INT AUTO_INCREMENT PRIMARY KEY, restaurant_id INT, day INT, open INT, close INT)"
    cursor.execute(day_table_create_command)


def load():
    REST_INSERT_COMMAND = "INSERT INTO " + \
        REST_TABLE_NAME + " (name) VALUES (%s)"
    
    WORKING_HOURS_INSERT_COMMAND = "INSERT INTO " + DAY_TABLE_NAME + \
        " (restaurant_id, day, open, close) VALUES (%s, %s, %s, %s)"

    print("\nLoading data...")
    try:
        db = mysql.connector.connect(
            host=db_config.HOST,
            user=db_config.USER,
            password=db_config.PASSWORD,
            database=db_config.DATABASE
        )
        cursor = db.cursor()
        drop_existing_table_and_create(cursor)
        try:
            with open("data.csv", "r") as data_file:
                csv_reader = csv.reader(data_file, delimiter=',')
                for row in csv_reader:
                    name = row[0]
                    cursor.execute(REST_INSERT_COMMAND, (name,))

                    working_hours = row[1]
                    restaurant_id = cursor.lastrowid

                    queries = process_working_hours(working_hours)

                    for query in queries:
                        cursor.execute(WORKING_HOURS_INSERT_COMMAND,
                                       (restaurant_id, query[0], query[1], query[2]))
        except:
            print("Error loading csv file")

        db.commit()
        print("\nLoading finished")
    except:
        print("Error connecting to the database")
    input("Press enter to continue")


def search_db(day_of_week, requested_time):
    db = mysql.connector.connect(
        host=db_config.HOST,
        user=db_config.USER,
        password=db_config.PASSWORD,
        database=db_config.DATABASE
    )
    cursor = db.cursor()

    SEARCH_QUERY = "SELECT r.name FROM " + REST_TABLE_NAME + " r JOIN " + DAY_TABLE_NAME + \
        " o ON r.id=o.restaurant_id WHERE %s>=o.open AND %s<=o.close AND day=%s"
    cursor.execute(SEARCH_QUERY, (requested_time, requested_time, day_of_week))

    result = cursor.fetchall()
    return result
