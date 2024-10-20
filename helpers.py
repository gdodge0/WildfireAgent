from datetime import datetime

def pretty_date_time(date_str):
    # Convert the string to a datetime object
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")

    # Get current date
    now = datetime.now()

    # Determine if the date is today
    if dt.date() == now.date():
        day_str = "today"
    else:
        day_str = dt.strftime("%m/%d")

    # Format the time in a 12-hour format with AM/PM
    time_str = dt.strftime("%I:%M %p").lstrip('0')  # remove leading zero

    # Combine time and day information
    if day_str == "today":
        return f"{time_str} {day_str}"
    else:
        return f"{time_str} on {day_str}"

