from __future__ import print_function
import socket
import sys
import os
from datetime import datetime

try:
    raw_input
except NameError:
    raw_input = input

# Enable ANSI colors on Windows cmd
if os.name == 'nt':
    os.system('')

# Colors
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
CYAN = '\033[36m'
RESET = '\033[0m'
BOLD = '\033[1m'

def run_single_scan(remoteServer=None):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(BOLD + YELLOW + "=== Single-Threaded Port Scanner ===" + RESET + "\n")

    if not remoteServer:
        try:
            remoteServer = raw_input(CYAN + "[?] Enter a remote host to scan: " + RESET)
        except (KeyboardInterrupt, EOFError):
            print("\n" + RED + "[-] Scan aborted." + RESET)
            return

    if not remoteServer.strip():
        print(RED + "[-] Hostname cannot be empty." + RESET)
        return

    print(YELLOW + "[*] Resolving host..." + RESET)
    try:
        remoteServerIP = socket.gethostbyname(remoteServer)
    except socket.gaierror:
        print(RED + "[-] Hostname could not be resolved. Exiting." + RESET)
        return

    print("-" * 50)
    print(GREEN + "[+] Target IP  : " + RESET + remoteServerIP)
    print(GREEN + "[+] Start Time : " + RESET + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print(YELLOW + "[*] Scanning ports 1 to 8887..." + RESET)
    print("-" * 50)

    t1 = datetime.now()

    try:
        for port in range(1, 8888):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print(GREEN + "[+] Port {}: \t Open".format(port) + RESET)
            sock.close()

    except KeyboardInterrupt:
        print("\n" + RED + "[-] Scan interrupted (Ctrl+C)." + RESET)
        return

    except socket.error:
        print(RED + "[-] Connection error occurred." + RESET)
        return

    t2 = datetime.now()
    total = t2 - t1
    print("-" * 50)
    print(GREEN + "[+] Scanning Completed in: " + RESET + str(total))
    print("-" * 50)
    
    try:
        raw_input("\n" + YELLOW + "Press Enter to return to main menu..." + RESET)
    except (KeyboardInterrupt, EOFError):
        pass

if __name__ == '__main__':
    run_single_scan()
