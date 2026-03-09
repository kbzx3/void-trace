import os,time,shutil
from datetime import datetime

class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    WHITE = "\033[97m"

white = Color.WHITE
red = Color.RED
color = Color()
module_display_name = "Addon Manager"
BEFORE = "["
AFTER = "]"
ADD = "[+]"
ERROR = "[!]"
INPUT = "[?]"
description = '''
Description:
A file-system utility that interfaces with the shutil and os modules to manage the utils/ directory. 
It performs absolute path moves for adding new modules and unlinks files for removal, requiring a 
program restart to re-initialize the dynamic import loop in main.py
Usage:
When prompted, type 'A' if you want to Add a new tool, or 'R if you want to Remove one.
Type the full location (path) of the .py file on your computer.
Important: You must close and restart the program to see your changes in the menu
'''
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
