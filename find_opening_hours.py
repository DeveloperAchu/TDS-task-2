# this function calculates the opening time and closing time in minutes of the day and append that to
# the list whose reference is passed
def find_opening_hours(day_index, queries, open_at, open_at_meridiem, close_at, close_at_meridiem):
    # start by initializing that the opening time is at the 0th minute of the day
    opening_time = 0
    # split the time at : which separates the hour and minute of the day
    opening_time_split = open_at.split(":")

    # if the opening meridiem is pm and the opening hour is less than 12, this means the restaurant is opening afternoon
    # so add 12 hours converted to minutes to the opening time
    if open_at_meridiem == "pm" and int(opening_time_split[0]) < 12:
        opening_time += (12 * 60)

    # add the hours converted to minutes to the opening time
    opening_time += (int(opening_time_split[0]) * 60)
    if len(opening_time_split) > 1:
        # if the time has minutes mentioned, add that minutes as it is
        opening_time += int(opening_time_split[1])

    # this flag tracks whether the restaurant is open after midnight
    add_to_next_day = False
    
    # start by initializing that the closing time is at the 0th minute of the day
    closing_time = 0
    # if the closing meridiem is pm, add 12 hours converted to minutes to the closing time
    if close_at_meridiem == "pm":
        closing_time += (12 * 60)

    # split the time at : which separates the hour and minute of the day
    closing_time_split = close_at.split(":")
    # add the hours converted to minutes to the closing time
    closing_time += (int(closing_time_split[0]) * 60)
    if len(closing_time_split) > 1:
        # if the time has minutes mentioned, add that minutes as it is
        closing_time += int(closing_time_split[1])

    # if the closing time is am and the calculated closing time in minutes is less than opening time in minutes,
    # this means the restaurant is open after midnight
    if close_at_meridiem == "am" and closing_time < opening_time:
        # set the flag
        add_to_next_day = True
        # set the next day's closing time at the calculated closing time
        next_day_closing_time = closing_time
        # set the current day's closing time at 1440 which is the total minutes in a day (24x60)
        closing_time = 1440

    # insert the details to queries list as a tuple
    queries.append((day_index, opening_time, closing_time))

    # if the restaurant is open after midnight,
    if add_to_next_day:
        # next days opening time is 0th minute of the day. that is 12:00 am
        opening_time = 0
        # set closing time as the closing time calculated earlier
        closing_time = next_day_closing_time
        # find the next day. if the day index is greater than 6, rotate the days index
        next_day = day_index + 1
        if next_day > 6:
            next_day -= 7

        # insert the details to queries list as a tuple
        queries.append((next_day, opening_time, closing_time))