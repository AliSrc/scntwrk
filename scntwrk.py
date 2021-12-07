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

notFoundnmap = os.popen('which nmap').read()
notFoundfiglet = os.popen('which figlet').read()

# Check if system is Linux or MacOS
if platform == "Linux" or platform == "linux2":
    if not notFoundnmap:
        os.system("sudo pacman -S nmap")
    if not notFoundfiglet:
        os.system("sudo pacman -S figlet")
    os.system("clear")
    os.system("figlet Scanning")
    print("Your operating system is Linux " + dist)
    os.system("sudo nmap -sn " + local_ip +"/24")
elif platform == "Darwin":
    if not notFoundnmap:
        os.system("brew install nmap")
    if not notFoundfiglet:
        os.system("brew install figlet")
    os.system("clear")
    os.system("figlet Scanning")
    print("Your ip-address is: " + local_ip)
    print("Your operating system is MacOS " + dist)
    os.system("sudo nmap -sn " + local_ip +"/24")

print("Scanning is now finished!")
