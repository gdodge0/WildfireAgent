from datetime import datetime
import pytz


def pretty_date_time(date_str, tz='America/Los_Angeles'):
    # Parse the string as UTC time
    utc = pytz.utc
    dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    dt_utc = utc.localize(dt)  # Localize as UTC time

    # Convert UTC to PST (Pacific Standard Time)
    local_tz = pytz.timezone(tz)
    dt_localized = dt_utc.astimezone(local_tz)

    # Get current date in PST
    now_pst = datetime.now(local_tz)

    # Determine if the date is today
    if dt_localized.date() == now_pst.date():
        day_str = "today"
    else:
        day_str = dt_localized.strftime("%m/%d")

    # Format the time in a 12-hour format with AM/PM
    time_str = dt_localized.strftime("%I:%M %p").lstrip('0')  # remove leading zero

    # Combine time and day information
    if day_str == "today":
        return f"{time_str} {day_str}"
    else:
        return f"{time_str} on {day_str}"
