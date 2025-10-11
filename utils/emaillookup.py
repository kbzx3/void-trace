import requests
from bs4 import BeautifulSoup
import datetime

# ---------------- Colors & Symbols ----------------
BEFORE = "["
AFTER = "]"
BEFORE_GREEN = "[+]"
AFTER_GREEN = "]"
ADD = "[+]"
ERROR = "[!]"
INFO = "[~]"
INPUT = "[?]"
GEN_VALID = "[VALID]"
GEN_INVALID = "[INVALID]"
WAIT = "[WAIT]"
white = "\033[97m"
red = "\033[91m"
reset = "\033[0m"

# ---------------- Helpers ----------------
def current_time_hour():
    return datetime.datetime.now().strftime("%H:%M:%S")

# Dummy placeholders for your custom functions
def Slow(msg): print(msg)
def Censored(email): pass
def Continue(): pass
def Reset(): pass
def Error(e): print(f"{ERROR} {e}")
def Title(msg): print(f"{INFO} {msg}")

# ---------------- Email Checker Functions ----------------
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

def Instagram(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/'
        }
        response = session.get("https://www.instagram.com/accounts/emailsignup/", headers=headers)
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        token = session.cookies.get('csrftoken', None)
        if not token:
            return "Error: Token Not Found."

        headers["x-csrftoken"] = token
        response = session.post(
            url="https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
            headers=headers,
            data={"email": email}
        )
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        if "Another account is using the same email." in response.text or "email_is_taken" in response.text:
            return True
        return False
    except Exception as e:
        return f"Error: {e}"

def Twitter(email):
    try:
        response = requests.get(
            url="https://api.twitter.com/i/users/email_available.json",
            params={"email": email}
        )
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        return response.json().get("taken", False)
    except Exception as e:
        return f"Error: {e}"

def Pinterest(email):
    try:
        response = requests.get(
            "https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/",
            params={"source_url": "/", "data": f'{{"options": {{"email": "{email}"}}, "context": {{}}}}'}
        )
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        data = response.json().get("resource_response", {})
        if data.get("message") == "Invalid email.":
            return False
        return data.get("data", False)
    except Exception as e:
        return f"Error: {e}"

def Imgur(email):
    try:
        session = requests.Session()
        headers = {'User-Agent': user_agent}
        session.get("https://imgur.com/register?redirect=%2Fuser", headers=headers)
        response = session.post(
            'https://imgur.com/signin/ajax_email_available',
            headers={**headers, "X-Requested-With": "XMLHttpRequest"},
            data={"email": email}
        )
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        available = response.json().get('data', {}).get("available", True)
        return not available
    except Exception as e:
        return f"Error: {e}"

def Patreon(email):
    try:
        response = requests.post(
            'https://www.plurk.com/Users/isEmailFound',
            data={"email": email},
            headers={'User-Agent': user_agent}
        )
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        return "True" in response.text
    except Exception as e:
        return f"Error: {e}"

def Spotify(email):
        try:
            session = requests.Session()
        
            headers = {
                'User-Agent': user_agent,
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'DNT': '1',
                'Connection': 'keep-alive',
            }
            
            params = {
                'validate': '1',
                'email': email,
            }

            response = session.get('https://spclient.wg.spotify.com/signup/public/v1/account',
                    headers=headers,
                    params=params)
            if response.status_code == 200:
                if response.json()["status"] == 1:
                    return False
                elif response.json()["status"] == 20:
                    return True
                else:
                    return False
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"

def FireFox(email):
    try:
        session = requests.Session()

        data = {
            "email": email
        }

        response = session.post(
            "https://api.accounts.firefox.com/v1/account/status",
            data=data
        )

        if response.status_code == 200:
            if "false" in response.text:
                return False
            elif "true" in response.text:
                return True
            else:
                return False
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def LastPass(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.5',
            'Referer': 'https://lastpass.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }
        params = {
            'check': 'avail',
            'skipcontent': '1',
            'mistype': '1',
            'username': email,
        }
        
        response = session.get(
            'https://lastpass.com/create_account.php?check=avail&skipcontent=1&mistype=1&username='+str(email).replace("@", "%40"),       
            params=params,
            headers=headers)
        
        if response.status_code == 200:
            if "no" in response.text:
                return True
            elif "emailinvalid" in response.text:
                return False
            elif "ok" in response.text:
                return False
            else:
                return False
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
        
def Archive(email):
    try:
        session = requests.Session()

        headers = {
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en,en-US;q=0.5',
            'Content-Type': 'multipart/form-data; boundary=---------------------------',
            'Origin': 'https://archive.org',
            'Connection': 'keep-alive',
            'Referer': 'https://archive.org/account/signup',
            'Sec-GPC': '1',
            'TE': 'Trailers',
        }

        data = '-----------------------------\r\nContent-Disposition: form-data; name="input_name"\r\n\r\nusername\r\n-----------------------------\r\nContent-Disposition: form-data; name="input_value"\r\n\r\n' + email + \
            '\r\n-----------------------------\r\nContent-Disposition: form-data; name="input_validator"\r\n\r\ntrue\r\n-----------------------------\r\nContent-Disposition: form-data; name="submit_by_js"\r\n\r\ntrue\r\n-------------------------------\r\n'

        response = session.post('https://archive.org/account/signup', headers=headers, data=data)
        if response.status_code == 200:
            if "is already taken." in response.text:
                return True
            else:
                return False
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
        
def PornHub(email):
    try:
        session = requests.Session()

        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en,en-US;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = session.get("https://www.pornhub.com/signup", headers=headers)
        if response.status_code == 200:
            token = BeautifulSoup(response.content, features="html.parser").find(attrs={"name": "token"})

            if token is None:
                return "Error: Token Not Found."
            
            token = token.get("value")
        else:
            return f"Error: {response.status_code}"

        params = {
            'token': token,
        }

        data = {
            'check_what': 'email',
            'email': email
        }

        response = session.post(
            'https://www.pornhub.com/user/create_account_check',
            headers=headers,
            params=params,
            data=data
        ) 
        if response.status_code == 200:
            if response.json()["error_message"] == "Email has been taken.":
                return True
            elif "Email has been taken." in response.text:
                return True
            else:
                return False
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
        
def Xnxx(email):
    try:
        session = requests.Session()

        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-en',
            'Host': 'www.xnxx.com',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive'
        }
        
        cookie = session.get('https://www.xnxx.com', headers=headers)

        if cookie.status_code == 200:
            if not cookie:
                return "Error: Cookie Not Found."
        else:
            return f"Error: {cookie.status_code}"
        
        headers['Referer'] = 'https://www.xnxx.com/video-holehe/palenath_fucks_xnxx_with_holehe'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        email = email.replace('@', '%40')

        response = session.get(f'https://www.xnxx.com/account/checkemail?email={email}', headers=headers, cookies=cookie.cookies)
        
        if response.status_code == 200:
            try:
                if response.json()['message'] == "This email is already in use or its owner has excluded it from our website.":
                    return True
                elif response.json()['message'] == "Invalid email address.": 
                    return False
            except:
                pass
            if response.json()['result'] == "false":
                return True
            elif response.json()['code'] == 1:
                return True
            elif response.json()['result'] == "true":
                return False
            elif response.json()['code'] == 0:
                return False  
            else:
                return False
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
        
def Xvideo(email):
    try:
        session = requests.Session()

        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'https://www.xvideos.com/',
        }

        params = {
            'email': email,
        }

        response = session.get('https://www.xvideos.com/account/checkemail', headers=headers, params=params)
        if response.status_code == 200:
            try:
                if response.json()['message'] == "This email is already in use or its owner has excluded it from our website.": 
                    return True
                elif response.json()['message'] == "Invalid email address.": 
                    return False
            except: 
                pass    
            if response.json()['result'] == "false":
                return True
            elif response.json()['code'] == 1:
                return True
            elif response.json()['result'] == "true":
                return False
            elif response.json()['code'] == 0:
                return False
            else:
                return False
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"



def emaillookup():
    Title("Email Tracker")
    Slow("[INFO] Initializing email scan...")
    email = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Email -> {reset}")
    Censored(email)
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning...")

    sites = [
        Instagram, Twitter, Pinterest, Imgur, Patreon, Spotify, FireFox, LastPass, Archive, PornHub, Xnxx, Xvideo]
    site_founds = []
    found = 0
    not_found = 0
    unknown = 0
    error_count = 0

    for site in sites:
        result = site(email)
        if result is True:
            print(f"{BEFORE_GREEN + current_time_hour() + AFTER_GREEN} {GEN_VALID} {site.__name__}: {white}Found{red}")
            site_founds.append(site.__name__)
            found += 1
        elif result is False:
            print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} {site.__name__}: {white}Not Found{red}")
            not_found += 1
        elif result is None:
            print(f"{BEFORE + current_time_hour() + AFTER} {GEN_INVALID} {site.__name__}: {white}Unknown{red}")
            unknown += 1
        else:
            print(f"{BEFORE + current_time_hour() + AFTER} {ERROR} {site.__name__}: {white + str(result)}")
            error_count += 1

    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} Total Found ({white}{found}{red}): {white}" + ", ".join(site_founds))
    print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Not Found: {white}{not_found}{red} Unknown: {white}{unknown}{red} Error: {white}{error_count}{red}")

    Continue()
    Reset()