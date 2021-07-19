from find_opening_hours import find_opening_hours
from date_to_day_dict import date_to_day_dict

# this function process the working hours that are in the csv file.
# the function cleans the data and return a list of tuples having the values to be inserted on to the
# restaurants_on_day_table
def process_working_hours(value):
    queries = []

    # we start by splitting the value on / which is used to mention multiple days of the week and working hours
    # if there are no / in the value, we get the value in the 0th position of the split list
    value_split = value.split("/")
    # we then iterate through the split list. this list now contains the working hours for a day or range of days
    for v in value_split:
        # strip off any extra leading or trailing white spaces
        v = v.strip()

        # split this details at white space. this will lead us to 2 cases based on our dataset.
        details_list = v.split(" ")
        # length of this split list is either 6 or 7
        # length = 6 means that the date range is clean and the time mentioned is applicable to a day or a range of days
        # length = 7 means that there is a jump in the days. that means there are multiple days or range of days
        # with the same opening time and closing time.
        # data values in the split list with length = 6
        # 0 => day or day range
        # 1 => opening time
        # 2 => opening time meridiem
        # 3 => a hyphen
        # 4 => closing time
        # 5 => closing time meridiem
        # 
        # # data values in the split list with length = 7
        # 0 => first set of day or day range
        # 1 => second set of day or day range
        # 2 => opening time
        # 3 => opening time meridiem
        # 4 => a hyphen
        # 5 => closing time
        # 6 => closing time meridiem
        # 
        # based on this pattern, we parse the data
        
        if len(details_list) == 6:
            first_days = details_list[0].split("-")
            # get the first working day of the week using the date_to_day_dict providing the value from the csv file
            first_start_day_index = date_to_day_dict[first_days[0]]
            # if the list after splitting at - has length greater than 1, this means that this is a range of days
            if len(first_days) > 1:
                first_end_day_index = date_to_day_dict[first_days[1]] + 1
            else:
                # if it is a single day, end day is considers 1 day after today to better iterate through the days
                first_end_day_index = date_to_day_dict[first_days[0]] + 1

            # iterate through the range of days
            for i in range(first_start_day_index, first_end_day_index):
                # this function calculates the opening time and closing time in minutes of the day and append
                # that to the queries. since python lists are mutable, passing queries list to this function
                # actually passes the list reference and alter the original list
                find_opening_hours(
                    i, 
                    queries, 
                    details_list[1], 
                    details_list[2], 
                    details_list[4], 
                    details_list[5]
                )
        elif len(details_list) == 7:
            # same process as above is handled here but the index of the details list are different.
            # also, we get 2 sets of days or range of days. this is marked with first and second prefix
            first_days = details_list[0].replace(",", "").split("-")
            first_start_day_index = date_to_day_dict[first_days[0]]
            if len(first_days) > 1:
                first_end_day_index = date_to_day_dict[first_days[1]] + 1
            else:
                first_end_day_index = date_to_day_dict[first_days[0]] + 1

            for i in range(first_start_day_index, first_end_day_index):
                find_opening_hours(
                    i, 
                    queries, 
                    details_list[2], 
                    details_list[3], 
                    details_list[5], 
                    details_list[6]
                )
            
            second_days = details_list[1].split("-")
            second_start_day_index = date_to_day_dict[second_days[0]]
            if len(second_days) > 1:
                second_end_day_index = date_to_day_dict[second_days[1]] + 1
            else:
                second_end_day_index = date_to_day_dict[second_days[0]] + 1

            for i in range(second_start_day_index, second_end_day_index):
                find_opening_hours(
                    i,
                    queries,
                    details_list[2], 
                    details_list[3], 
                    details_list[5], 
                    details_list[6]
                )

    return queries