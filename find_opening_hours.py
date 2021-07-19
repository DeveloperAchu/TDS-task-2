def find_opening_hours(day_index, queries, open_at, open_at_meridiem, close_at, close_at_meridiem):
    opening_time = 0
    opening_time_split = open_at.split(":")
    if open_at_meridiem == "pm" and int(opening_time_split[0]) < 12:
        opening_time += (12 * 60)

    opening_time += (int(opening_time_split[0]) * 60)
    if len(opening_time_split) > 1:
        opening_time += int(opening_time_split[1])

    add_to_next_day = False
    closing_time = 0
    if close_at_meridiem == "pm":
        closing_time += (12 * 60)

    closing_time_split = close_at.split(":")
    closing_time += (int(closing_time_split[0]) * 60)
    if len(closing_time_split) > 1:
        closing_time += int(closing_time_split[1])

    if close_at_meridiem == "am" and closing_time < opening_time:
        add_to_next_day = True
        next_day_closing_time = closing_time
        closing_time = 1440

    # insert to current day here
    queries.append((day_index, opening_time, closing_time))

    if add_to_next_day:
        opening_time = 0
        closing_time = next_day_closing_time
        next_day = day_index + 1
        if next_day > 6:
            next_day -= 7

        # insert to next day here
        queries.append((next_day, opening_time, closing_time))