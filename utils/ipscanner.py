import socket
import subprocess
import sys
import ssl
import requests
from requests.exceptions import RequestException
import concurrent.futures
import time
from datetime import datetime

class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    WHITE = "\033[97m"

white = Color.WHITE
red = Color.RED
color = Color()

BEFORE = "["
AFTER = "]"
ADD = "[+]"
ERROR = "[!]"
INPUT = "[?]"
WAIT = "[~]"

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Slow(text, delay=0.05):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def Error(e):
    print(f"{ERROR} {e}")

banner = "=== IP Info Scanner ==="
scan_banner = "=== Starting IP Scan ==="

def ip_type(ip):
    if ':' in ip:
        t = "IPv6"
    elif '.' in ip:
        t = "IPv4"
    else:
        t = "Unknown"
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} IP Type: {white}{t}{red}")

def ip_ping(ip):
    try:
        if sys.platform.startswith("win"):
            result = subprocess.run(['ping', '-n', '1', ip], capture_output=True, text=True, timeout=1)
        else:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, text=True, timeout=1)
        ping_status = "Succeed" if result.returncode == 0 else "Fail"
    except:
        ping_status = "Fail"

    print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Ping: {white}{ping_status}{red}")

def ip_dns(ip):
    try:
        dns, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
    except:
        dns = None
    if dns:
        print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} DNS: {white}{dns}{red}")

def ip_host_info(ip):
    api_url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(api_url, timeout=3)
        api = response.json()
    except RequestException:
        api = {}

    for key, label in [("country", "Host Country"), ("hostname", "Host Name"),
                       ("org", "Host ISP"), ("asn", "Host AS")]:
        value = api.get(key)
        if value:
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} {label}: {white}{value}{red}")

def ssl_certificate_check(ip):
    port = 443
    try:
        sock = socket.create_connection((ip, port), timeout=2)
        context = ssl.create_default_context()
        with context.wrap_socket(sock, server_hostname=ip) as ssock:
            cert = ssock.getpeercert()
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} SSL Certificate: {white}{cert}{red}")
    except Exception as e:
        print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} SSL Certificate Check Failed: {white}{e}{red}")

def ip_port(ip):
    port_protocol_map = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 69: "TFTP",
        80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP", 194: "IRC", 389: "LDAP",
        443: "HTTPS", 161: "SNMP", 3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis",
        1521: "Oracle DB", 3389: "RDP"
    }

    port_list = list(port_protocol_map.keys())

    def scan_port(ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                protocol = port_protocol_map.get(port, "Unknown")
                print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Port: {white}{port}{red} Status: {white}Open{red} Protocol: {white}{protocol}{red}")
            sock.close()
        except:
            pass

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(scan_port, ip, port) for port in port_list]
        concurrent.futures.wait(futures)

def ipscanner():
    Slow(banner)
    ip = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} IP -> {color.RESET}")
    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Gathering Information...{color.RESET}")
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} IP: {white}{ip}{red}")

    ip_type(ip)
    ip_ping(ip)
    ip_dns(ip)
    ip_port(ip)
    ip_host_info(ip)
    ssl_certificate_check(ip)

