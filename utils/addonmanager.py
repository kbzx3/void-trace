import os,time,shutil
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

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Slow(text, delay=0.05):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def Error(message):
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} {message}")

folder = os.path.dirname(__file__)

def addonmanager():
    
    addrem= input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Do you want to add an addon or remove an addon (A/R) -> {red}")
    if addrem.lower() == 'a':
       filepath = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter Addon file path -> {red}")
       shutil.move(filepath,folder)
       print(f"{BEFORE}{current_time_hour()}{AFTER} Added Addon, please restrart the program{red}")
    elif addrem.lower() == 'r':
        filepath = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Enter Addon file path -> {red}")
        os.remove(filepath)
        print(f"{BEFORE}{current_time_hour()}{AFTER} Removed Addon, please restrart the program{red}")
    else: print(f"{BEFORE}{current_time_hour()}{AFTER}{ERROR}Please enter a valid choice.{red}")
