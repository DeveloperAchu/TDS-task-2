import mysql.connector
import csv

import db_config
from process_working_hours import process_working_hours

# define the table names
REST_TABLE_NAME = "restaurants_table"
DAY_TABLE_NAME = "restaurants_on_day_table"

# this function drops the table if exists and create the tables to load data again
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


# this function loads data to the table using SQL insert command
def load():
    REST_INSERT_COMMAND = "INSERT INTO " + \
        REST_TABLE_NAME + " (name) VALUES (%s)"

    WORKING_HOURS_INSERT_COMMAND = "INSERT INTO " + DAY_TABLE_NAME + \
        " (restaurant_id, day, open, close) VALUES (%s, %s, %s, %s)"

    print("\nLoading data...")
    try:
        # establish a connection to the mysql database server using the credentials defined in db_config.py
        db = mysql.connector.connect(
            host=db_config.HOST,
            user=db_config.USER,
            password=db_config.PASSWORD,
            database=db_config.DATABASE
        )

        # get a cursor from the db object to control the execution of SQL commands
        cursor = db.cursor()
        # invoke the above defined function to delete any data that is currently in the DB
        drop_existing_table_and_create(cursor)
        try:
            # open the csv file in read mode. For convenience, the file name has been changed to data.csv
            with open("data.csv", "r") as data_file:
                # using the csv module that is imported, read the data file
                csv_reader = csv.reader(data_file, delimiter=',')
                # iterate through each row in the file
                for row in csv_reader:
                    # name of the restaurant is in the 0th column of the row
                    name = row[0]
                    # insert the name of the restaurant to restaurants_table. this will generate an id that we access using lastrowid on the cursor
                    cursor.execute(REST_INSERT_COMMAND, (name,))
                    restaurant_id = cursor.lastrowid

                    # the working hours is in the 1st column of the row
                    working_hours = row[1]
                    # outsource the processing of this working hours. this function returns a list of tuples
                    # containing the index of the day of the week, opening hour in minutes of the day, and
                    # closing hour in minutes of the day
                    queries = process_working_hours(working_hours)

                    # iterate through the tuple list and insert the details to restaurants_on_day_table
                    for query in queries:
                        cursor.execute(WORKING_HOURS_INSERT_COMMAND,
                                       (restaurant_id, query[0], query[1], query[2]))
        except:
            # if there is any error reading the csv file
            print("Error loading csv file")

        # finally, we commit the changes to the DB. this call will make the required changes in the DB.
        db.commit()
        print("\nLoading finished")
    except:
        # if there is any error connecting to the database
        print("Error connecting to the database")
    input("Press enter to continue")


# this function search the db for the open restaurants using the day of the week index and time. the time
# is converted to minutes of the day before invoking this function
def search_db(day_of_week, requested_time):
    # establish a connection to the mysql database server using the credentials defined in db_config.py
    db = mysql.connector.connect(
        host=db_config.HOST,
        user=db_config.USER,
        password=db_config.PASSWORD,
        database=db_config.DATABASE
    )
    # get a cursor from the db object to control the execution of SQL commands
    cursor = db.cursor()

    # the select query is done by joining the restaurants_table and restaurants_on_day_table. the joining is done
    # on the rows of restaurants_on_day_table which has the requested_time value greater than or equal to the
    # restaurant opening time in minutes and less than or equal to restaurant closing time in minutes. this result
    # is then joined with the restaurants_table on matching the restaurant ids.
    SEARCH_QUERY = "SELECT r.name FROM " + REST_TABLE_NAME + " r JOIN " + DAY_TABLE_NAME + \
        " o ON r.id=o.restaurant_id WHERE %s>=o.open AND %s<=o.close AND day=%s"
    cursor.execute(SEARCH_QUERY, (requested_time, requested_time, day_of_week))

    # we fetch all the results that are in the cursor and return the value
    result = cursor.fetchall()
    return result
