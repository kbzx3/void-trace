import requests
import time
import random
import os
import hashlib
from datetime import datetime

module_display_name = "Email Lookup"

BEFORE = "["
AFTER = "]"
BEFORE_GREEN = "\033[92m["
AFTER_GREEN = "]\033[0m"
ERROR = "[!]"
INFO = "[~]"
INPUT = "[?]"
GEN_VALID = "[VALID]"
GEN_INVALID = "[INVALID]"
WAIT = "[WAIT]"

white = "\033[97m"
red = "\033[91m"
reset = "\033[0m"

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Continue():
    input(f"\n{BEFORE}{current_time_hour()}{AFTER} {INFO} {white}Press Enter to return to main menu...{reset}")

def Reset():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')

def _selenium_check(fn):
    def wrapper(*args, **kwargs):
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            return fn(*args, webdriver=webdriver, Options=Options,
                      Service=Service, By=By, Wait=WebDriverWait, EC=EC, **kwargs)
        except ImportError:
            return "Error: selenium not installed (pip install selenium)"
        except Exception as e:
            return f"Error: {e}"
    wrapper.__name__ = fn.__name__
    return wrapper

def _make_driver(webdriver, Options, Service):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(options=opts)


class EmailScanner:
    def __init__(self):
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept-Language': 'en-US,en;q=0.9',
        })


    def Twitter(self, email):
        try:
            r = self.session.get(
                "https://api.twitter.com/i/users/email_available.json",
                params={"email": email}, timeout=10)
            if r.status_code != 200:
                return f"Error {r.status_code}"
            return r.json().get("taken", False)
        except Exception as e:
            return f"Error: {e}"

    def Spotify(self, email):
        try:
            r = self.session.get(
                'https://spclient.wg.spotify.com/signup/public/v1/account',
                params={'validate': '1', 'email': email}, timeout=10)
            if r.status_code == 200:
                return r.json().get("status") == 20
            return f"Error {r.status_code}"
        except Exception as e:
            return f"Error: {e}"

    def Archive(self, email):
        try:
            url = "https://archive.org/account/signup"
            self.session.get(url, timeout=10)
            r = self.session.post(url, data={
                "input_name": "username",
                "input_value": email,
                "input_validator": "true",
                "submit_by_js": "true"
            }, timeout=10)
            return "is already taken" in r.text
        except Exception as e:
            return f"Error: {e}"

    def Duolingo(self, email):
        try:
            r = self.session.get(
                'https://www.duolingo.com/2017-06-30/users',
                params={'email': email}, timeout=10)
            if r.status_code == 200:
                return len(r.json().get('users', [])) > 0
            return f"Error {r.status_code}"
        except Exception as e:
            return f"Error: {e}"

    def FireFox(self, email):
        try:
            r = self.session.post(
                "https://api.accounts.firefox.com/v1/account/status",
                json={"email": email}, timeout=10)
            if r.status_code == 200:
                return r.json().get("exists", False)
            return f"Error {r.status_code}"
        except Exception as e:
            return f"Error: {e}"

    def Gravatar(self, email):
        try:
            h = hashlib.md5(email.strip().lower().encode()).hexdigest()
            r = self.session.get(f'https://www.gravatar.com/{h}.json', timeout=10)
            if r.status_code == 200:
                return True
            if r.status_code == 404:
                return False
            return f"Error {r.status_code}"
        except Exception as e:
            return f"Error: {e}"

    def Plurk(self, email):
        try:
            r = self.session.post(
                'https://www.plurk.com/Users/isEmailFound',
                data={"email": email}, timeout=10)
            if r.status_code != 200:
                return f"Error {r.status_code}"
            return "True" in r.text
        except Exception as e:
            return f"Error: {e}"

    def LastPass(self, email):
        try:
            self.session.headers.update({
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://lastpass.com/'
            })
            fe = email.replace("@", "%40")
            r = self.session.get(
                f'https://lastpass.com/create_account.php'
                f'?check=avail&skipcontent=1&mistype=1&username={fe}',
                timeout=10)
            if r.status_code == 200:
                return "no" in r.text.lower()
            return f"Error {r.status_code}"
        except Exception as e:
            return f"Error: {e}"






    @_selenium_check
    def Pinterest(self, email, webdriver=None, Options=None, Service=None,
                  By=None, Wait=None, EC=None):
        import json as _json
        from urllib.parse import quote
        driver = _make_driver(webdriver, Options, Service)
        try:
            driver.get("https://www.pinterest.com/")
            time.sleep(3)
            encoded = quote(f'{{"options":{{"email":"{email}"}},"context":{{}}}}')
            driver.get(
                f"https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/"
                f"?source_url=%2F&data={encoded}"
            )
            time.sleep(2)
            raw = driver.find_element(By.TAG_NAME, "body").text.strip()
            try:
                data = _json.loads(raw)
                resp = data.get("resource_response", {})
                if resp.get("message") == "Invalid email.":
                    return False
                result = resp.get("data")
                if result is True:
                    return True
                if result is False:
                    return False
                if isinstance(result, dict):
                    return result.get("exists", False)
                return False
            except Exception:
                return '"data": true' in raw or '"exists": true' in raw
        finally:
            driver.quit()

    @_selenium_check
    def Imgur(self, email, webdriver=None, Options=None, Service=None,
              By=None, Wait=None, EC=None):
        import json as _json
        from urllib.parse import quote
        driver = _make_driver(webdriver, Options, Service)
        try:
            driver.get("https://imgur.com/")
            time.sleep(2)
            driver.get(f"https://imgur.com/signin/ajax_email_available?email={quote(email)}")
            time.sleep(1)
            raw = driver.find_element(By.TAG_NAME, "body").text.strip()
            try:
                data = _json.loads(raw)
                return not data.get('data', {}).get('available', True)
            except Exception:
                return "false" in raw.lower()
        finally:
            driver.quit()


def emaillookup():
    print(f"{INFO} {white}Email Tracker initialized.{reset}")
    email = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Email -> {reset}").strip()

    if not email or "@" not in email:
        print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} {white}Invalid email format.{reset}")
        Continue()
        return

    print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} {white}Scanning (this may take a moment)...{reset}\n")

    scanner = EmailScanner()

    sites = {
        "Twitter":       scanner.Twitter,
        "Spotify":       scanner.Spotify,
        "Archive":       scanner.Archive,
        "Duolingo":      scanner.Duolingo,
        "FireFox":       scanner.FireFox,
        "Gravatar":      scanner.Gravatar,
        "Plurk":         scanner.Plurk,
        "LastPass":      scanner.LastPass,
        "Pinterest":     scanner.Pinterest,
        "Imgur":         scanner.Imgur,
    }

    site_founds = []
    found = 0
    not_found = 0
    error_count = 0

    for site_name, check_function in sites.items():
        result = check_function(email)

        if result is True:
            print(f"{BEFORE_GREEN}{current_time_hour()}{AFTER_GREEN} {GEN_VALID} {site_name}: {white}Found{reset}")
            site_founds.append(site_name)
            found += 1
        elif result is False:
            print(f"{BEFORE}{current_time_hour()}{AFTER} {GEN_INVALID} {site_name}: {white}Not Found{reset}")
            not_found += 1
        else:
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} {site_name}: {white}{result}{reset}")
            error_count += 1

    print(f"\n{BEFORE}{current_time_hour()}{AFTER} {INFO} Total Found ({white}{found}{reset}): {white}{', '.join(site_founds) if site_founds else 'None'}{reset}")
    print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Not Found: {white}{not_found}{reset} Error: {white}{error_count}{reset}")

    Continue()
    Reset()