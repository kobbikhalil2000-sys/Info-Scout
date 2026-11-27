from datetime import datetime

def start(info):
    try:
        with open("/proc/stat", "r") as f:
            info["Time"]["Boot-time"] = "No boot-time found. Did you forget to boot your system?"
            for line in f:
                # The kernel records the boot time as a Unix timestamp on the 'btime' line.
                if line.startswith("btime"):
                    raw_data = line.split()[1]             # Grab the timestamp string
                    raw_time = int(raw_data)               # Convert string to integer
                    real_time = datetime.fromtimestamp(raw_time) # Convert Unix time to a datetime object
                    info["Time"]["Boot-time"] = f_date(real_time) # Format and store it
                    break # Stop reading the file, we found what we needed
    except FileNotFoundError:
        # Default fallback string in case the file is missing or unreadable.
        info["Time"]["Boot-time"] = "Couldn't read kernel statistics. Nice permissions, genius."
    return info



def f_date(amount):
    # :02d is the format specifier that forces single-digit numbers to have a leading zero (e.g., 05).
    return f"{amount.year}-{amount.month:02d}-{amount.day:02d} " \
           f"{amount.hour:02d}:{amount.minute:02d}:{amount.second:02d}"