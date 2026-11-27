import subprocess as Srun
import os

def activate(info):
    os_id = info["System"]["Os id"]
    match os_id:
        case "arch" | "manjaro" | "endeavouros" | "garuda" | "artix":
            try:
                package_list = os.listdir("/var/lib/pacman/local")

            except FileNotFoundError:
                return "Unknown", "How can you break that !"
            count = len(package_list)
            return f"{count}", "pacman"

        case "debian" | "ubuntu" | "linuxmint" | "pop" | "kali" | "elementary" | "zorin":
            try:
                package_list = os.listdir("/var/lib/dpkg/info")

            except FileNotFoundError:
                return "Unknown", "How can you break that !"
            count = 0
            for f in package_list:
                if f.endswith(".list"):
                    count += 1
            return f"{count}", "apt/dpkg"

        case "fedora" | "rhel" | "centos" | "rocky" | "almalinux" | "opensuse-leap" |\
            "opensuse-tumbleweed" | "sles":
            try:
                output = Srun.run(["rpm", "-qa"], capture_output=True, text=True, timeout=5, check=True)
                package_list = output.stdout.splitlines()
                count = len(package_list)
                return f"{count}", "rpm"

            except FileNotFoundError:
                return "No rpm executable. Did you lose it ?", "Unknown"

            except Srun.TimeoutExpired:
                return "RPM took too long. I have better things to do.", "Unknown"

            except Srun.CalledProcessError:
                return "RPM crashed. Impressive work.", "Unknown"

        case _:
            return "Unsupported distro. Your choices concern me.", "Unknown"