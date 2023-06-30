#!/usr/bin/env python3

import socket
import platform
import distro
import subprocess
import argparse
import ipaddress
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        return local_ip
    except socket.error as e:
        logging.error("Error getting local IP address: %s", str(e))
        print("Error getting local IP address:", str(e))
        return None

def get_system_info():
    """Get information about the system"""
    system = platform.system()
    dist = distro.name()
    return system, dist

def clear_screen():
    """Clear the terminal screen"""
    subprocess.run(["clear"])

def perform_network_scan(ip_address, ports):
    """Perform a network scan using nmap"""
    try:
        command = ["nmap", "-p", ports, "-oN", f"scan_{ip_address}.txt", ip_address]
        subprocess.run(command, check=True)
        logging.info("Scan completed for IP address: %s", ip_address)
    except subprocess.CalledProcessError as e:
        logging.error("Error performing network scan for IP address %s: %s", ip_address, e)
        print(f"Error performing network scan for IP address {ip_address}: {e}")

def validate_ip_address(ip_address):
    """Validate the IP address format"""
    try:
        ipaddress.IPv4Address(ip_address)
        return True
    except ipaddress.AddressValueError:
        return False

def discover_hosts(subnet):
    """Discover active hosts in the network"""
    try:
        command = ["nmap", "-sn", subnet]
        output = subprocess.run(command, capture_output=True, text=True).stdout
        active_hosts = []
        lines = output.split("\n")
        for line in lines:
            if "Nmap scan report for" in line:
                parts = line.split(" ")
                if len(parts) > 4:
                    host = parts[4].strip()
                    active_hosts.append(host)
        return active_hosts
    except subprocess.CalledProcessError as e:
        logging.error("Error discovering hosts in subnet %s: %s", subnet, e)
        print(f"Error discovering hosts in subnet {subnet}: {e}")
        return []

def scan_network(subnet, ports, max_threads=10):
    """Scan the network for active hosts"""
    active_hosts = discover_hosts(subnet)
    if not active_hosts:
        print("No active hosts found in the network.")
        return

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        scan_tasks = []
        for host in active_hosts:
            scan_task = executor.submit(perform_network_scan, host, ports)
            scan_tasks.append(scan_task)

        print("Scanning in progress...\n")

        for future in as_completed(scan_tasks):
            future.result()

    print("\nScanning is now finished!")

def main():
    # Set up logging
    logging.basicConfig(filename='scan.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Network scanning script")
    parser.add_argument("--local", action="store_true", help="Scan the local network")
    parser.add_argument("--ip", help="Specify an IP address to scan")
    parser.add_argument("--ports", "-p", nargs="?", default="1-1000", help="Ports to scan (default: 1-1000)")
    parser.add_argument("--threads", "-t", type=int, default=10, help="Maximum number of threads for scanning (default: 10)")
    args = parser.parse_args()

    # Get local IP address
    local_ip = get_local_ip()

    # Get system information
    system, dist = get_system_info()

    # Clear the screen
    clear_screen()

    # Print system information
    subprocess.run(["figlet", "Scanning"])
    print("Local IP address:", local_ip)
    print("OS:", dist, "\n")

    # Scan the network
    if args.local:
        subnet = ".".join(local_ip.split(".")[:3]) + ".0/24"
        scan_network(subnet, args.ports, args.threads)
    elif args.ip:
        ip = args.ip
        if validate_ip_address(ip):
            perform_network_scan(ip, args.ports)
        else:
            print("Invalid IP address format.")
    else:
        print("Please specify either --local or --ip option.")

if __name__ == "__main__":
    main()
