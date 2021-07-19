from find_opening_hours import find_opening_hours
from date_to_day_dict import date_to_day_dict

def process_working_hours(value):
    queries = []

    value_split = value.split("/")
    queries = []
    for v in value_split:
        v = v.strip()
        details_list = v.split(" ")
        
        if len(details_list) == 6:
            first_days = details_list[0].split("-")
            first_start_day_index = date_to_day_dict[first_days[0]]
            if len(first_days) > 1:
                first_end_day_index = date_to_day_dict[first_days[1]] + 1
            else:
                first_end_day_index = date_to_day_dict[first_days[0]] + 1

            for i in range(first_start_day_index, first_end_day_index):
                find_opening_hours(
                    i, 
                    queries, 
                    details_list[1], 
                    details_list[2], 
                    details_list[4], 
                    details_list[5]
                )
        elif len(details_list) == 7:
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