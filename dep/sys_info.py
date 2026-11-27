import platform

def start(info):
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

    return info