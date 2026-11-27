import os
from dep.helpers import get_packs

def start(info):
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
    info["Software"]["Packages"], info["Software"]["Pack Manager"] = get_packs.activate(info)
    return info