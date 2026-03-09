import socket
import time
from datetime import datetime

# -------- Styling & helpers --------
class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    WHITE = "\033[97m"

white = Color.WHITE
red = Color.RED
color = Color()
module_display_name = "IP Ping Tool"
description = '''
Description:
A low-level network utility using the socket module to initiate AF_INET SOCK_STREAM connections. 
It calculates TCP latency by measuring the time delta between the connection start and the 
successful transmission of a specified byte payload.

Usage:
1. Enter the target IP address you want to test.
2. Enter the Port number (press Enter for the default, Port 80).
3. Enter the amount of Bytes to send (press Enter for 64 bytes).
4. The tool will report the connection speed in "ms" (milliseconds).
'''
BEFORE = "["
AFTER = "]"
ADD = "[+]"
ERROR = "[!]"
INPUT = "[?]"

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Slow(text, delay=0.05):

    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def Error(message):
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} {message}")

wifi_banner = "=== TCP Ping Tool ==="

# -------- Ping function --------
def ping_ip(hostname, port, bytes_to_send):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        start_time = time.time()
        sock.connect((hostname, port))
        data = b'\x00' * bytes_to_send
        sock.sendall(data)
        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000  # ms
        print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Hostname: {white}{hostname}{red} time: {white}{elapsed_time:.2f}ms{red} port: {white}{port}{red} bytes: {white}{bytes_to_send}{red} status: {white}succeed{red}")
        sock.close()
    except Exception as e:
        elapsed_time = 0
        print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Hostname: {white}{hostname}{red} time: {white}{elapsed_time}ms{red} port: {white}{port}{red} bytes: {white}{bytes_to_send}{red} status: {white}fail{red} ({e})")

# -------- Main --------
def ipping():
    Slow(wifi_banner)

    while True:
        hostname = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} IP (or 'q' to return to menu) -> {Color.RESET}").strip().lower()
        if hostname == 'q':
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Returning to menu.")
            return

        while True:
            port_input = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Port (enter for default, 'q' to return to menu) -> {Color.RESET}").strip().lower()
            if port_input == 'q':
                print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Returning to menu.")
                return
            try:
                port = int(port_input) if port_input else 80
                if port < 1 or port > 65535:
                    Error("Port must be between 1 and 65535.")
                    continue
                break
            except ValueError:
                Error("Invalid port entered! Please enter a number or press Enter for default.")
                continue

        while True:
            bytes_input = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Bytes (enter for default, 'q' to return to menu) -> {Color.RESET}").strip().lower()
            if bytes_input == 'q':
                print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Returning to menu.")
                return
            try:
                bytes_to_send = int(bytes_input) if bytes_input else 64
                if bytes_to_send < 1:
                    Error("Bytes must be a positive number.")
                    continue
                break
            except ValueError:
                Error("Invalid bytes entered! Please enter a number or press Enter for default.")
                continue

        print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Press 'q' to return to menu or Ctrl+C to stop.")
        
        while True:
            try:
                user_input = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Press Enter to ping or 'q' to return to menu -> {Color.RESET}").strip().lower()
                if user_input == 'q':
                    print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Returning to menu.")
                    return
                ping_ip(hostname, port, bytes_to_send)
            except KeyboardInterrupt:
                print(f"\n{BEFORE}{current_time_hour()}{AFTER} {ADD} Returning to menu (Ctrl+C detected).")
                return

