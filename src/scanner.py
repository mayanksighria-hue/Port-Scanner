from __future__ import print_function
import socket
import subprocess
import sys
from datetime import datetime
import json
import os
import threading
try:
    import builtins
except ImportError:
    import __builtin__ as builtins

from multi.scanner_thread import split_processing
from single.scanner import run_single_scan
from ipscanner import run_ip_scan

try:
    raw_input
except NameError:
    raw_input = input

exc = getattr(builtins, "IOError", "FileNotFoundError")

# Enable ANSI colors on Windows cmd
if os.name == 'nt':
    os.system('')

# Colors
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Global variable accessed by the threaded scan target
remoteServerIP = ""

def get_absolute_path(relative_path):
    dir = os.path.dirname(os.path.abspath(__file__))
    split_path = relative_path.split("/")
    absolute_path = os.path.join(dir, *split_path)
    return absolute_path

def scan_port(ports, range_low, range_high):
    global remoteServerIP
    try:
        for port in range(range_low, range_high):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                print(GREEN + "[+] Port {}: \t Open".format(port) + RESET)
            sock.close()

    except KeyboardInterrupt:
        print("\n" + RED + "[-] Scan interrupted (Ctrl+C)." + RESET)
        sys.exit()
    except socket.gaierror:
        print(RED + "[-] Hostname could not be resolved. Exiting." + RESET)
        sys.exit()
    except socket.error:
        print(RED + "[-] Connection error occurred." + RESET)
        sys.exit()

def run_multi_port_scan(remoteServer=None):
    global remoteServerIP
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(BOLD + YELLOW + "=== Multithreaded Port Scanner ===" + RESET + "\n")

    if not remoteServer:
        try:
            remoteServer = raw_input(CYAN + "[?] Enter a remote host to scan (e.g. google.com): " + RESET)
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

    t1 = datetime.now()

    try:
        with open(get_absolute_path('../config.json')) as config_file:
            config = json.load(config_file)
        range_high = int(config['range']['high'])
        range_low = int(config['range']['low'])
        CONST_NUM_THREADS = int(config['thread']['count'])
    except IOError:
        print(RED + "[-] config.json file not found" + RESET)
        return
    except ValueError:
        print(RED + "[-] Kindly check the json file for appropriateness of range" + RESET)
        return

    print("-" * 50)
    print(GREEN + "[+] Target Host   : " + RESET + remoteServer)
    print(GREEN + "[+] Target IP     : " + RESET + remoteServerIP)
    print(GREEN + "[+] Thread Count  : " + RESET + str(CONST_NUM_THREADS))
    print(GREEN + "[+] Scan Range    : " + RESET + "{}-{}".format(range_low, range_high))
    print(YELLOW + "[*] Scanning ports..." + RESET)
    print("-" * 50)

    ports = list(range(range_low, range_high, 1))
    split_processing(ports, CONST_NUM_THREADS, scan_port, range_low, range_high)

    t2 = datetime.now()
    total = t2 - t1
    print("-" * 50)
    print(GREEN + "[+] Scanning Completed in: " + RESET + str(total))
    print("-" * 50)

    try:
        raw_input("\n" + YELLOW + "Press Enter to return to main menu..." + RESET)
    except (KeyboardInterrupt, EOFError):
        pass

def show_banner():
    banner = r"""
  _____           _    _____                                 
 |  __ \         | |  / ____|                                
 | |__) |__  _ __| |_| (___   ___ __ _ _ __  _ __   ___ _ __ 
 |  ___/ _ \| '__| __|\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 | |  | (_) | |  | |_ ____) | (_| (_| | | | | | | |  __/ |   
 |_|   \___/|_|   \__|_____/ \___\__,_|_| |_|_| |_|\___|_|   
    """
    print(BOLD + CYAN + banner + RESET)
    print(BOLD + RED + "                   Version : 2.0.0" + RESET)
    print(BOLD + GREEN + "     [-] Tool enhanced with premium CLI style" + RESET)
    print("-" * 60 + "\n")

def show_about():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(BOLD + YELLOW + "=== About PortScanner ===" + RESET + "\n")
    print("PortScanner is an interactive multithreaded network scanning utility.")
    print("Features:")
    print("  - Multithreaded & Single-threaded port scanning")
    print("  - Live IP subnet range detection")
    print("  - Dynamic Web UI (Flask-based representation)")
    print("\nCredits to the original creators and authors.")
    print("-" * 50)
    try:
        raw_input(YELLOW + "Press Enter to return to main menu..." + RESET)
    except (KeyboardInterrupt, EOFError):
        pass

def run_web_server():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(BOLD + YELLOW + "=== Launching Web Server (Flask) ===" + RESET + "\n")
    print(GREEN + "[+] Starting Web UI server..." + RESET)
    print(YELLOW + "[*] Access the interface at: http://127.0.0.1:5000/" + RESET)
    print(RED + "[!] Press Ctrl+C in the terminal to stop the server." + RESET + "\n")
    
    try:
        from mainScanner import app
        # Disable Flask debug mode pin / reloading console logs clashing in interactive shell
        app.run(debug=True, use_reloader=False)
    except ImportError:
        print(RED + "[-] mainScanner.py or flask module not found." + RESET)
        try:
            raw_input(YELLOW + "Press Enter to return to main menu..." + RESET)
        except (KeyboardInterrupt, EOFError):
            pass
    except KeyboardInterrupt:
        print("\n" + RED + "[-] Web server stopped." + RESET)
        try:
            raw_input(YELLOW + "Press Enter to return to main menu..." + RESET)
        except (KeyboardInterrupt, EOFError):
            pass

def main_menu():
    while True:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        
        show_banner()
        
        print(CYAN + "[::] Select An Option [::]" + RESET + "\n")
        print(GREEN + "  [01]" + RESET + " Multithreaded Port Scanner")
        print(GREEN + "  [02]" + RESET + " Single-threaded Port Scanner")
        print(GREEN + "  [03]" + RESET + " Multithreaded Live Host Scanner")
        print(GREEN + "  [04]" + RESET + " Launch Flask Web Application")
        print(GREEN + "  [99]" + RESET + " About PortScanner")
        print(GREEN + "  [00]" + RESET + " Exit")
        print()
        
        try:
            choice = raw_input(CYAN + "[-] Select an option : " + RESET).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n" + RED + "[*] Exiting... Goodbye!" + RESET)
            break
            
        if choice == "01" or choice == "1":
            run_multi_port_scan()
        elif choice == "02" or choice == "2":
            run_single_scan()
        elif choice == "03" or choice == "3":
            run_ip_scan()
        elif choice == "04" or choice == "4":
            run_web_server()
        elif choice == "99":
            show_about()
        elif choice == "00" or choice == "0":
            print(GREEN + "[*] Exiting... Goodbye!" + RESET)
            break
        else:
            print(RED + "[-] Invalid choice! Please select a valid option." + RESET)
            import time
            time.sleep(1.5)

if __name__ == '__main__':
    main_menu()
