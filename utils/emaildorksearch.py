import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from datetime import datetime
import time
import urllib.parse


white = "\033[97m"
red = "\033[91m"
reset = "\033[0m"

BEFORE = "["
AFTER = "]"
ADD = "[+]"
INPUT = "[?]"
WAIT = "[~]"

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Slow(text, delay=0.03):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

banner = "=== Email Dork Search ==="

def emaildorksearch():
    Slow(banner)
    email = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Enter email -> {white}").strip().lower()
    print(reset, end="")

    if not email or " " in email:
        print(f"{BEFORE}{current_time_hour()}{AFTER} {red}Invalid email. Provide a non-empty single token (no spaces).{reset}")
        return

    
    query = urllib.parse.quote_plus(f"intext:{email}")
    url = f"https://html.duckduckgo.com/html?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9"
    }

    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Searching...: {white}{email}{reset}")

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"{BEFORE}{current_time_hour()}{AFTER} {red}Request failed: {e}{reset}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    
    for r in soup.select(".result"):
        a = r.select_one(".result__a")
        if not a:

            a = r.select_one("a")
        if a:
            title = a.get_text(strip=True)
            link = a.get("href")
            if link and title:
                results.append((title, link))

    if not results:
        print(f"{BEFORE}{current_time_hour()}{AFTER} {red}No results found or site blocked the request.{reset}")
        return

    print(f"\n{BEFORE}{current_time_hour()}{AFTER} {ADD} Top results for {white}{email}{reset}\n")
    print(tabulate(results, headers=["Title", "URL"], tablefmt="grid"))
