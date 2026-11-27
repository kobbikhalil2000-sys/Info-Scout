
import platform
from datetime import datetime
import os
import subprocess as Srun

# Assign colors
RED = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Main dictionary to store all system data.
# Structuring it this way makes it easy to export to JSON later.
info = {"System": {}, "Time": {}, "Software": {}, "Important": {"Sister name": "Cammous"}}




def sys_info():
    # Reads the Linux distribution details from /etc/os-release
    try:
        data = platform.freedesktop_os_release()
        info["System"]["Os name"] = data["NAME"]
        info["System"]["Os id"] = data["ID"]
    except (OSError, KeyError):
        info["System"]["Os name"] = "Your OS is playing hide and seek. Couldn't find its name."
        info["System"]["Os id"] = "No ID either. Very suspicious."

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
        info["Time"]["Uptime"] = "Time itself refused to cooperate."




def boot_time():
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




def software_info():
    # First the Init System (e.g. systemd, runit...)
    try:
        with open("/proc/1/comm", "r") as f:
            file = f.read().strip()
            info["Software"]["Init System"] = file

    except (FileNotFoundError, ValueError):
        info["Software"]["Init System"] = "Couldn't identify PID 1. What have you done?"

    # Get the Shell (I know it's SO short.. But that's all)
    info["Software"]["Shell"] = os.environ.get("SHELL", "No shell information. Are you communicating through telepathy?")

    # Now, we get the number of bullshit the user has installed
    info["Software"]["Packages"] = get_packs()




def get_packs():
    os_id = info["System"]["Os id"]
    match os_id:
        case "arch" | "manjaro" | "endeavouros" | "garuda" | "artix":
            package_list = os.listdir("/var/lib/pacman/local")
            count = len(package_list)
            return f"{count}, (pacman)"

        case "debian" | "ubuntu" | "linuxmint" | "pop" | "kali" | "elementary" | "zorin":
            package_list = os.listdir("/var/lib/dpkg/info")
            count = 0
            for f in package_list:
                if f.endswith(".list"):
                    count += 1
            return f"{count}, (apt/dpkg)"

        case "fedora" | "rhel" | "centos" | "rocky" | "almalinux":
            try:
                output = Srun.run(["rpm", "-qa"], capture_output=True, text=True, timeout=5, check=True)
                package_list = output.stdout.splitlines()
                count = len(package_list)
                return f"{count}, (rpm)"

            except FileNotFoundError:
                return "No rpm executable. Did you lose it ?"

            except Srun.TimeoutExpired:
                return "RPM took too long. I have better things to do."

            except Srun.CalledProcessError:
                return "RPM crashed. Impressive work."

        case "opensuse-leap" | "opensuse-tumbleweed" | "sles":
            return "Not supported yet. Patience, exotic creature."

        case _:
            return "Unsupported distro. Your choices concern me."




def f_uptime(amount):
    # Extract the milliseconds by getting the decimal part and multiplying by 1000.
    mils = (amount - int(amount)) * 1000
    
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

    # round() prevents floating-point inaccuracies from showing up (e.g., 74.99999).
    return (
        f"{days} days, {hours} hours, "
        f"{mins} mins, {secs} secs, {round(mils)} milliseconds"
    )




def f_date(amount):
    # :02d is the format specifier that forces single-digit numbers to have a leading zero (e.g., 05).
    return f"""{amount.year}-{amount.month:02d}-{amount.day:02d}
    {amount.hour:02d}:{amount.minute:02d}:{amount.second:02d}"""




def Print(data):
    for category, keys in data.items():
        print(f"{RED}======== {category} ========{RESET}")
        for key, value in keys.items():
            print(f"{BLUE}{key}{RESET}:",
                  f"{value}")




if __name__ == "__main__":
    try:
        # Execute the data collection functions
        sys_info()
        uptime()
        boot_time()
        software_info()
    except Exception as e:
        print(f"Well, you broke something. Here's the evidence: {e}",
              "I'm sure you'll figure it out."
              )

# Output the final data structure
Print(info)
