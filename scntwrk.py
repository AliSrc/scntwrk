#!/usr/bin/env python3

import os
import socket
import platform
import distro

# Get local ip-address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = (s.getsockname()[0])

# Get information about the system
platform = platform.system()

# Get distro infomation
dist = distro.name()

# Check if system is Linux or MacOS
if platform == "Linux" or platform == "linux2":
    os.system("clear")
    print("Your operating system is Linux " + dist)
    os.system("sudo nmap -sn " + local_ip +"/24")
elif platform == "Darwin":
    os.system("clear")
    print("Your ip-address is: " + local_ip)
    print("Your operating system is MacOS " + dist)
    os.system("sudo nmap -sn " + local_ip +"/24")

print("Scanning is now finished!")
