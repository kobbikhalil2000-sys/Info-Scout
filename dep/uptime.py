from datetime import timedelta


def start(info: dict) -> dict:
    # /proc/uptime contains the system uptime in seconds as a float.
    try:
        with open("/proc/uptime") as uptime_file:
            uptime_data = uptime_file.read()
        
        # Grab the first number before the space and convert it to a float.
        real_time = float(uptime_data.split()[0])

        # Send the raw seconds to the formatter function and store the result.
        info["Time"]["Uptime"] = f_uptime(real_time)

    except (FileNotFoundError, ValueError):
        info["Time"]["Uptime"] = "Time itself refused to cooperate."
    return info




def f_uptime(amount: float) -> str: # BTW "f" stands for "format"
    # We basicly are transforming it to milliseconds
    # cuz the file returns time in seconds
    duration = timedelta(milliseconds=round(amount * 1000))

    # Days first
    days = duration.days

    # We get secs to use in out math
    secs_m = duration.seconds # BTW "m" stands for "math"

    # Now hours, and we get the amount of hours and the resting amount of time
    hours, remainder = divmod(secs_m, 3600)

    # Now minutes and secs for display
    mins, secs = divmod(remainder, 60)

    return f"{days} day ," if days == 1 else f"{days} days, " \
           f"{hours} hours, " \
            f"{mins} mins, " \
            f"{secs} secs."