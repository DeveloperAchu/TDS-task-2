from datetime import datetime

from db_handler import search_db
from date_to_day_dict import date_to_day_dict


def process_user_selection(option):
    if option == 1:
        print("\nPlease enter the date in format DD/MM/YYYY")
        input_date = input("Date: ")
        date_split = input_date.split("/")
        try:
            date = datetime(year=int(date_split[2]), month=int(
                date_split[1]), day=int(date_split[0]))
            day_of_week = date.weekday()
        except:
            print("Invalid date")
            input("Press enter to continue")
            return
    elif option == 2:
        print("\nPlease enter day of the week as Mon, Tue, ...")
        input_day_of_week = input("Day of week: ")
        try:
            day_of_week = date_to_day_dict[input_day_of_week]
        except:
            print("Invalid day")
            input("Press enter to continue")
            return
    else:
        exit()
    
    try:
        print("\nPlease enter the time in format hh:mm a")
        input_time = input("Time: ")
        time = datetime.strptime(input_time, '%I:%M %p')
        full_time = str(time).split(" ")[1].split(":")

        requested_time = (int(full_time[0]) * 60) + int(full_time[1])
        try:
            result = search_db(day_of_week, requested_time)
            print("\nOpen restaurants:\n")
            for res in result:
                print(res[0])
        except:
            print("Failed to fetch data from database")
        input("\nPress enter to continue")       
    except:
        print("Invalid time")
        input("Press enter to continue")


def search():
    while True:
        print("\nPlease select an option and press enter to continue:")
        print("1. Provide Date (DD/MM/YYYY)")
        print("2. Provide day of the week (Mon, Tue, ...)")
        print("3. Exit")
        user_input = input("option: ")
        if user_input.isdigit():
            option = int(user_input)
            if option >= 1 and option <= 3:
                process_user_selection(option)
                break
            else:
                print("Invalid option. Please enter digit (1, 2 or 3)")
                input("Press enter to continue")
        else:
            print("Invalid input. Please enter digit (1, 2 or 3)")
            input("Press enter to continue")
