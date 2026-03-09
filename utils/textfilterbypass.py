import time
from datetime import datetime
class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    WHITE = "\033[97m"

module_display_name = "Message filter bypass"
description = '''
Description:
A character-mapping script that replaces standard ASCII Latin characters with visually 
identical Unicode homoglyphs from the Cyrillic and Greek alphabets. This circumvents 
automated string-matching filters by using different character codes.

Usage:
1. Type the message you want to send past a filter.
2. The tool generates a version that looks normal but uses special characters.
3. Copy the encoded text from the box and paste it where needed.
'''
white = Color.WHITE
red = Color.RED

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
char = {
    'A': 'А',  
    'B': 'Β',  
    'C': 'С',  
    'E': 'Ε',  
    'H': 'Н',  
    'I': 'І',  
    'J': 'Ј', 
    'K': 'Κ',  
    'M': 'М',  
    'N': 'Ν',     
    'O': 'О',
    'P': 'Р', 
    'S': 'Ѕ',  
    'T': 'Т',  
    'X': 'Χ',      
    'a': 'а',  
    'c': 'с',  
    'e': 'е',  
    'i': 'і',  
    'j': 'ј',  
    'o': 'о',  
    'p': 'р',  
    's': 'ѕ',  
    'x': 'х',  
    'y': 'у',  
}
def replacechar(text: str) -> str:

    return ''.join(char.get(ch, ch) for ch in text)

def textfilterbypass():
    msg= input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Enter message to encode with unicode bypass -> {red}")
    msglen=len(msg)
    msglen_=msglen+15
    space= 35 - msglen_
    space2 = msglen_-35
    space3 = ' '*space2
    if msglen_>=35:
        print(f"\n{red}╔{'═'*msglen_}╗{Color.RESET}")
        print(f"║{BEFORE}{current_time_hour()}{AFTER} {ADD} Copy and paste it:{space3}  ║ {red}")
        print(f"║{BEFORE}{current_time_hour()}{AFTER} {ADD} {replacechar(msg)+' '*space}║")
        print(f"{red}╚{'═'*msglen_}╝{Color.RESET}\n")
    else: 
        print(f"\n{red}╔{'═'*35}╗{Color.RESET}")
        print(f"║{BEFORE}{current_time_hour()}{AFTER} {ADD} Copy and paste it:  ║ {red}")
        print(f"║{BEFORE}{current_time_hour()}{AFTER} {ADD} {replacechar(msg)+' '*space}║")
        print(f"{red}╚{'═'*35}╝{Color.RESET}\n")       