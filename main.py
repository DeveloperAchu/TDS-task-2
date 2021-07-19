import os

from db_handler import load
from search_data import search

# This function navigates the user to the appropriate function
def process_user_action(option):
    if option == 1:
        load()
    elif option == 2:
        search()
    else:
        exit()

# The program starts execution from this main function
# The main function listens for the uses's input. The user is expected to provide a digit as input
# 1 => Loading data from csv file to local mysql server
# 2 => Once the data has been loaded, user can select this option to search any open restaurants
# 3 => To exit the program, enter option 3
if __name__ == "__main__":    
    while True:
        # system call to clear the terminal based on the user's machine
        os.system('cls||clear')
        
        print("\nPlease select an option and press enter to continue:")
        print("1. Load data")
        print("2. Search restaurants")
        print("3. Exit")
        
        # Listen for user input here
        user_input = input("option: ")
        
        # Sanity check for user input
        if user_input.isdigit():
            option = int(user_input)

            # The input is processed only if it is in between 1 and 3
            if option >= 1 and option <= 3:
                process_user_action(option)
            else:
                print("Invalid option. Please enter digit (1, 2 or 3)")
                input("Press enter to continue")
        else:
            print("Invalid input. Please enter digit (1, 2 or 3)")
            input("Press enter to continue")