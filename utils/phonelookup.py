import phonenumbers
from phonenumbers import geocoder, carrier, timezone, NumberParseException
from tabulate import tabulate
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

def ErrorNumber():
    print(f"{ERROR} Invalid number entered!")

def Error(e):
    print(f"{ERROR} {e}")

banner = "=== Phone Info Checker ==="

# -------- Phone lookup function --------
def lookupnum(number):
    try:
        number = number.replace(" ", "").replace("-", "")

        # Only accept numbers with country code
        if not number.startswith("+"):
            return {"error": "Please only enter numbers with country code starting with '+'."}

        pnum = phonenumbers.parse(number)

        if not phonenumbers.is_possible_number(pnum) or not phonenumbers.is_valid_number(pnum):
            return {"error": "Please enter a valid number."}

        info = {
            "International Format": phonenumbers.format_number(pnum, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "National Format": phonenumbers.format_number(pnum, phonenumbers.PhoneNumberFormat.NATIONAL),
            "Country Code": pnum.country_code,
            "Region": phonenumbers.region_code_for_number(pnum),
            "Carrier": carrier.name_for_number(pnum, "en"),
            "Geocoder": geocoder.description_for_number(pnum, "en"),
            "Timezones": timezone.time_zones_for_number(pnum)
        }

        return info

    except NumberParseException as e:
        return {"error": str(e)}

# -------- CLI Table --------
def print_cli_table(number_info):
    if "error" in number_info:
        print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} {number_info['error']}")
    else:
        table = [[key, value] for key, value in number_info.items()]
        print("\nPhone Number Info\n" + "="*40)
        print(tabulate(table, headers=["Property", "Value"], tablefmt="grid"))

def numlookup():

    Slow(banner)

    number_input = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Phone number (with country code) -> {Color.RESET}")

    info = lookupnum(number_input)
    print_cli_table(info)


