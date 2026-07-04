from __future__ import print_function
import socket
from datetime import datetime
import json
import os
import sys
from multi.scanner_thread import split_processing

try:
    raw_input
except NameError:
    raw_input = input

try:
    xrange
except NameError:
    xrange = range

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

def get_absolute_path(relative_path):
    dir = os.path.dirname(os.path.abspath(__file__))
    split_path = relative_path.split("/")
    absolute_path = os.path.join(dir, *split_path)
    return absolute_path

def scan(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = sock.connect_ex((addr, 135))  # Port 135 is used for Windows live check
    if result == 0:
        return 1
    else:
        return 0

def run1(ips, range_low, range_high, net3):
    for ip in xrange(range_low, range_high):
        addr = net3 + str(ip)
        if scan(addr):
            print(GREEN + "[+] {} is live".format(addr) + RESET)

def run_ip_scan(net1=None):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(BOLD + YELLOW + "=== Multithreaded Live Host Scanner ===" + RESET + "\n")

    if not net1:
        try:
            net1 = raw_input(CYAN + "[?] Enter the IP address (e.g. 192.168.1.1): " + RESET)
        except (KeyboardInterrupt, EOFError):
            print("\n" + RED + "[-] Scan aborted." + RESET)
            return

    if not net1.strip():
        print(RED + "[-] IP address cannot be empty." + RESET)
        return

    net2 = net1.split('.')
    if len(net2) < 3:
        print(RED + "[-] Invalid IP address format." + RESET)
        return
    a = '.'
    net3 = net2[0] + a + net2[1] + a + net2[2] + a

    td1 = datetime.now()

    try:
        with open(get_absolute_path('../config.json')) as config_file:
            config = json.load(config_file)
        range_low = int(config['ipRange']['low'])
        range_high = int(config['ipRange']['high'])
        CONST_NUM_THREADS = int(config['thread']['count'])
    except IOError:
        print(RED + "[-] config.json file not found" + RESET)
        return
    except ValueError:
        print(RED + "[-] Kindly check the json file for appropriateness of range" + RESET)
        return

    print("-" * 50)
    print(GREEN + "[+] Subnet Target : " + RESET + net3 + "XXX")
    print(GREEN + "[+] Threads Count : " + RESET + str(CONST_NUM_THREADS))
    print(GREEN + "[+] Scan Range    : " + RESET + "{}-{}".format(range_low, range_high))
    print(YELLOW + "[*] Scanning active hosts..." + RESET)
    print("-" * 50)

    ips = list(range(range_low, range_high + 1))
    
    # Custom lambda-like target to pass net3 to run1
    def thread_target(ips, start, end):
        run1(ips, start, end, net3)

    split_processing(ips, CONST_NUM_THREADS, thread_target, range_low, range_high + 1)
    
    td2 = datetime.now()
    total = td2 - td1
    print("-" * 50)
    print(GREEN + "[+] Scanning completed in: " + RESET + str(total))
    print("-" * 50)

    try:
        raw_input("\n" + YELLOW + "Press Enter to return to main menu..." + RESET)
    except (KeyboardInterrupt, EOFError):
        pass

if __name__ == '__main__':
    run_ip_scan()
