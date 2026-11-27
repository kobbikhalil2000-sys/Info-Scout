import subprocess as Srun
import os

def activate(info):
    os_id = info["System"]["Os id"]
    match os_id:
        case "arch" | "manjaro" | "endeavouros" | "garuda" | "artix":
            package_list = os.listdir("/var/lib/pacman/local")
            count = len(package_list)
            return f"{count}", "pacman"

        case "debian" | "ubuntu" | "linuxmint" | "pop" | "kali" | "elementary" | "zorin":
            package_list = os.listdir("/var/lib/dpkg/info")
            count = 0
            for f in package_list:
                if f.endswith(".list"):
                    count += 1
            return f"{count}", "apt/dpkg"

        case "fedora" | "rhel" | "centos" | "rocky" | "almalinux":
            try:
                output = Srun.run(["rpm", "-qa"], capture_output=True, text=True, timeout=5, check=True)
                package_list = output.stdout.splitlines()
                count = len(package_list)
                return f"{count}", "rpm"

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