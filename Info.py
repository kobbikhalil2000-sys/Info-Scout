import platform
from datetime import datetime

info = {"System": {}, "Time": {}}


def sys_info():
    data = platform.freedesktop_os_release()

    info["System"]["Os name"] = data["NAME"]
    info["System"]["Os id"] = data["ID"]
    info["System"]["Kernel"] = platform.system()
    info["System"]["Kernel version"] = platform.release()
    info["System"]["Architecture"] = platform.machine()
    info["System"]["Host name"] = platform.node()


def uptime():
    with open("/proc/uptime") as uptime_file:
        uptime_data = uptime_file.read()

    real_time = float(uptime_data.split()[0])

    info["Time"]["Uptime"] = f_uptime(real_time)


def boot_time():
    info["Time"]["Boot-time"] = "An Error has occured.. Weird"
    with open("/proc/stat", "r") as file:
        for line in file:
            if line.startswith("btime"):
                raw_data = line.split()[1]
                raw_time = int(raw_data)
                real_time = datetime.fromtimestamp(raw_time)
                info["Time"]["Boot-time"] = f_date(real_time)


def f_uptime(amount):
    mils = (amount - int(amount)) * 100
    amount = int(amount)

    secs = amount % 60
    amount //= 60

    mins = amount % 60
    amount //= 60

    hours = amount % 24
    days = amount // 24

    return (
        f"{days} days, {hours} hours, "
        f"{mins} mins, {secs} secs, {round(mils)} milliseconds"
    )


def f_date(amount):
    return f"{amount.year}-{amount.month:02d}-{amount.day:02d} {amount.hour:02d}:{amount.minute:02d}:{amount.second:02d}"


if __name__ == "__main__":
    sys_info()
    uptime()
    boot_time()

print(info)