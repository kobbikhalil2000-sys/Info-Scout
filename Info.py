#! /usr/bin/env python3
from dep import sys_info, uptime, boot_time, software_info

# Assign colors
RED = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Main dictionary to store all system data.
# Structuring it this way makes it easy to export to JSON later.
info = {"System": {}, "Time": {}, "Software": {}, "Important": {"Sister name": "Cammous"}}


def Print(data):
    for category, keys in data.items():
        print(f"{RED}======== {category} ========{RESET}")
        for key, value in keys.items():
            print(f"{BLUE}{key}{RESET}:",
                  f"{value}")


if __name__ == "__main__":
    try:
        # Execute the data collection functions
        info = sys_info.start(info)
        info = uptime.start(info)
        info = boot_time.start(info)
        info = software_info.start(info)

        # Output the final data structure
        Print(info)

    except Exception as e:
        print(f"Well, you broke something. Here's the evidence: {e}",
              "I'm sure you'll figure it out."
              )

# Output the final data structure
Print(info)
