import platform
from datetime import datetime

# Main dictionary to store all system data.
# Structuring it this way makes it easy to export to JSON later.
info = {"System": {}, "Time": {}}


def sys_info():
    # Reads the Linux distribution details from /etc/os-release
    try:
        data = platform.freedesktop_os_release()
        info["System"]["Os name"] = data["NAME"]
        info["System"]["Os id"] = data["ID"]
    except (OSError, KeyError):
        info["System"]["Os name"] = "That didn't really work..."
        info["System"]["Os id"] = "That didn't work either..."

    info["System"]["Kernel"] = platform.system()
    info["System"]["Kernel version"] = platform.release()
    info["System"]["Architecture"] = platform.machine()
    info["System"]["Host name"] = platform.node()


def uptime():
    # /proc/uptime contains the system uptime in seconds as a float.
    try:
        with open("/proc/uptime") as uptime_file:
            uptime_data = uptime_file.read()
        
        # Grab the first number before the space and convert it to a float.
        real_time = float(uptime_data.split()[0])

        # Send the raw seconds to the formatter function and store the result.
        info["Time"]["Uptime"] = f_uptime(real_time)

    except (FileNotFoundError, ValueError):
        info["Time"]["Uptime"] = "An error occured"


def boot_time():
    try:
        with open("/proc/stat", "r") as f:
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
        info["Time"]["Boot-time"] = "An Error has occured.. Weird"


def f_uptime(amount):
    # Extract the milliseconds by getting the decimal part and multiplying by 100.
    mils = (amount - int(amount)) * 100
    
    # Remove the decimal from the total amount so we can do whole-number math.
    amount = int(amount)

    # Use modulo (%) to get the remainder (e.g., leftover seconds)
    # and floor division (//) to break the time down into smaller units.
    secs = amount % 60
    amount //= 60

    mins = amount % 60
    amount //= 60

    hours = amount % 24
    days = amount // 24

    # round() prevents floating-point inaccuracies from showing up (like 74.99999).
    return (
        f"{days} days, {hours} hours, "
        f"{mins} mins, {secs} secs, {round(mils)} milliseconds"
    )


def f_date(amount):
    # :02d is the format specifier that forces single-digit numbers to have a leading zero (e.g., 05).
    return f"{amount.year}-{amount.month:02d}-{amount.day:02d} {amount.hour:02d}:{amount.minute:02d}:{amount.second:02d}"


if __name__ == "__main__":
    # Execute the data collection functions
    sys_info()
    uptime()
    boot_time()

# Output the final data structure
print(info)