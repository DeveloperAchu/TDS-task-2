from datetime import datetime

from db_handler import search_db
from date_to_day_dict import date_to_day_dict

# This function receives the user input in the format selected by the user
def process_user_selection(option):
    if option == 1:
        print("\nPlease enter the date in format DD/MM/YYYY")
        input_date = input("Date: ")
        # split the date input at / to separate day, month, and year
        date_split = input_date.split("/")
        try:
            # try to create a datetime object with the details
            date = datetime(year=int(date_split[2]), month=int(
                date_split[1]), day=int(date_split[0]))
            # get the index of the day of the week
            day_of_week = date.weekday()
        except:
            # if the date input is an invalid date
            print("Invalid date")
            input("Press enter to continue")
            return
    elif option == 2:
        print("\nPlease enter a day of the week as Mon, Tue, ...")
        input_day_of_week = input("Day of week: ")
        try:
            # based on the user's input, map the day of the week to it's index using date_to_day_dict
            day_of_week = date_to_day_dict[input_day_of_week]
        except:
            # if no mapping is found exit here
            print("Invalid day")
            input("Press enter to continue")
            return
    else:
        exit()
    
    # if the date input is clear, get the user input for time. the time is expected to receive in
    # hh:mm a format. example: 12:30 pm
    try:
        print("\nPlease enter the time in format hh:mm a")
        input_time = input("Time: ")
        # create a datetime object using the input time
        time = datetime.strptime(input_time, '%I:%M %p')
        # get the time that is in the second part of the datetime object after the whitespace and split
        # that at : to get the hour and minute
        full_time = str(time).split(" ")[1].split(":")

        # calculate the requested time in minutes of the day by converting the time
        requested_time = (int(full_time[0]) * 60) + int(full_time[1])
        try:
            # search the DB with the input day of the week and requested time and get the results from DB
            result = search_db(day_of_week, requested_time)
            print("\nOpen restaurants:\n")
            # iterate through the results cursor. this is a tuple and the 0th element is the name of
            # restaurants open on that date and time
            for res in result:
                print(res[0])
        except:
            # if the program fails to fetch data from the DB
            print("Failed to fetch data from database")
        input("\nPress enter to continue")       
    except:
        # if the input time is invalid
        print("Invalid time")
        input("Press enter to continue")


# The function listens for the uses's input. The user is expected to provide a digit as input
# 1 => User choose to input a date in the DD/MM/YYYY format
# 2 => User choose to provide the day of the week as an abbreviated name
# 3 => To exit, enter option 3
def search():
    while True:
        print("\nPlease select an option and press enter to continue:")
        print("1. Provide Date (DD/MM/YYYY)")
        print("2. Provide a day of the week (Mon, Tue, ...)")
        print("3. Exit")
        
        # Listen for user input here
        user_input = input("option: ")

        # Sanity check for user input
        if user_input.isdigit():
            option = int(user_input)

            # The input is processed only if it is in between 1 and 3
            if option >= 1 and option <= 3:
                process_user_selection(option)
                break
            else:
                print("Invalid option. Please enter digit (1, 2 or 3)")
                input("Press enter to continue")
        else:
            print("Invalid input. Please enter digit (1, 2 or 3)")
            input("Press enter to continue")
