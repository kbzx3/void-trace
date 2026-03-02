#function may not accurately find all emails on all websites
import requests
from bs4 import BeautifulSoup
import datetime

module_display_name = "Email Lookup"
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

def GitHub(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json',
        }
        
        params = {'email': email}
        response = session.get('https://github.com/signup_check/email', headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'available' in data:
                return not data['available']
            return False
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def Discord(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Content-Type': 'application/json'
        }
        
        # Discord requires CAPTCHA for registration checking, making automated detection difficult
        # This checks if we can get past basic validation with the v9 API
        import random
        unique_id = random.randint(100000, 999999)
        data = {
            'email': email,
            'username': f'test{unique_id}',
            'password': 'TestPassword123!@#',
            'date_of_birth': '1995-01-15'
        }
        
        response = session.post('https://discord.com/api/v9/auth/register', headers=headers, json=data)
        
        # If we get a captcha-required error, the email likely exists (passed initial validation)
        if response.status_code == 400:
            resp_text = response.text.lower()
            if 'captcha' in resp_text:
                # Email passed validation, likely exists
                return True
            elif 'email' in resp_text and ('taken' in resp_text or 'already' in resp_text):
                return True
            else:
                return False
        # If status is not 400, return False
        return False
    except Exception as e:
        return f"Error: {e}"

def Slack(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json'
        }
        
        # Slack returns the email in response if it exists
        data = {'email': email}
        response = session.post(
            'https://slack.com/api/signup.checkEmail',
            headers=headers,
            data=data
        )
        
        if response.status_code == 200:
            try:
                resp_json = response.json()
                # If email exists, Slack returns: {'ok': True, 'email': 'user@example.com', 'challenge_response': True}
                # If email doesn't exist, it returns: {'ok': False, 'error': 'invalid_email'} or similar
                if resp_json.get('ok') == True and 'email' in resp_json:
                    return True
                return False
            except:
                pass
        
        return False
    except Exception as e:
        return f"Error: {e}"

def YouTube(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml',
            'Referer': 'https://accounts.google.com/signup'
        }
        
        # Google/YouTube uses accounts.google.com for signup
        data = {'email': email}
        response = session.post(
            'https://accounts.google.com/register/checkEmailAvailable',
            headers=headers,
            data=data
        )
        
        if response.status_code == 200:
            resp_text = response.text.lower()
            # If email is taken, Google returns specific indicators
            if 'taken' in resp_text or 'already' in resp_text or 'exists' in resp_text:
                return True
            # Check JSON response
            try:
                resp_json = response.json()
                return not resp_json.get('available', True)  # Return True if NOT available (exists)
            except:
                pass
        
        return False
    except Exception as e:
        return f"Error: {e}"

def Telegram(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json'
        }
        
        # Telegram's email signup check
        data = {'email': email}
        response = session.post(
            'https://web.telegram.org/api/auth/checkEmailAvailable',
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            try:
                resp_json = response.json()
                # If email exists, Telegram returns available: false
                if 'available' in resp_json:
                    return not resp_json.get('available', True)
                # Check for other indicators
                if 'error' in resp_json and 'exists' in resp_json.get('error', '').lower():
                    return True
                return False
            except:
                pass
        
        return False
    except Exception as e:
        return f"Error: {e}"

def LinkedIn(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json',
            'Referer': 'https://www.linkedin.com/'
        }
        
        # LinkedIn password reset check - if email exists
        data = {'email': email}
        response = session.post(
            'https://www.linkedin.com/identity/ajax/emailaddress',
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            resp_json = response.json()
            return resp_json.get('emailAddress') is not None or 'found' in response.text.lower()
        
        response = session.post(
            'https://api.linkedin.com/v2/auth/login',
            headers=headers,
            json={'username': email, 'password': 'dummy'}
        )
        return response.status_code in [401, 403, 200]
    except Exception as e:
        return f"Error: {e}"

def Amazon(email):
    try:
        session = requests.Session()
        headers = {'User-Agent': user_agent}
        
        data = {'email': email}
        response = session.post('https://www.amazon.com/ap/signin', headers=headers, data=data)
        
        if 'already' in response.text.lower() or 'exist' in response.text.lower():
            return True
        return False
    except Exception as e:
        return f"Error: {e}"

def Gmail(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Referer': 'https://accounts.google.com/',
        }
        
        data = {'email': email, 'checkConnection': 'youtube,1'}
        response = session.post('https://accounts.google.com/_/signin/sl/lookup', headers=headers, data=data)
        
        if 'email-not-found' not in response.text.lower() and response.text.strip() and response.status_code == 200:
            return True
        return False
    except Exception as e:
        return f"Error: {e}"

def Apple(email):
    try:
        session = requests.Session()
        headers = {'User-Agent': user_agent}
        
        data = {'email': email}
        response = session.post('https://appleid.apple.com/account', headers=headers, data=data)
        
        if 'already' in response.text.lower() or 'taken' in response.text.lower():
            return True
        return False
    except Exception as e:
        return f"Error: {e}"


# ==================== UTILITY FUNCTIONS ====================

def validate_email_format(email):
    """Validate basic email format before checking"""
    if '@' not in email or '.' not in email.split('@')[1]:
        return False
    return True

def is_valid_response(response):
    """Check if response is valid HTTP"""
    return response is not None and hasattr(response, 'status_code')

def retry_request(url, method='get', data=None, headers=None, max_retries=2):
    """Retry failed requests with exponential backoff"""
    import time
    for attempt in range(max_retries):
        try:
            session = requests.Session()
            if method.lower() == 'get':
                response = session.get(url, headers=headers, timeout=5)
            elif method.lower() == 'post':
                response = session.post(url, headers=headers, data=data, timeout=5, json=data)
            return response
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return None

def get_session_with_headers(user_agent_str):
    """Create a session with proper headers"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': user_agent_str,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    })
    return session

def parse_json_response(response):
    """Safely parse JSON response"""
    try:
        return response.json() if response else None
    except:
        return None

def check_email_in_response(email, response_text, keywords=None):
    """Check if email or keywords appear in response"""
    if not response_text:
        return False
    response_lower = response_text.lower()
    email_lower = email.lower()
    
    # Check if email is in response
    if email_lower in response_lower:
        return True
    
    # Check for common keywords
    if keywords:
        for keyword in keywords:
            if keyword.lower() in response_lower:
                return True
    
    return False

def extract_error_info(response):
    """Extract error information from response"""
    if not response:
        return "No response"
    if response.status_code == 429:
        return "Rate limited"
    if response.status_code == 403:
        return "Forbidden"
    if response.status_code == 404:
        return "Not found"
    if response.status_code >= 500:
        return "Server error"
    return f"Status {response.status_code}"


def emaillookup():
    Title("Email Tracker")
    Slow("[INFO] Initializing email scan...")
    email = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Email -> {reset}")
    Censored(email)
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Scanning...")

    sites = [
        Twitter, Pinterest, Imgur, Patreon, Spotify, FireFox, LastPass, Archive, GitHub, Discord, Slack,
        YouTube, Telegram, LinkedIn, Amazon, Apple
    ]
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