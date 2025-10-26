import time
from datetime import datetime
class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    WHITE = "\033[97m"



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
    """Replace letters with visually identical Unicode versions."""
    return ''.join(char.get(ch, ch) for ch in text)

def textfilterbypass():
    msg= input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Enter message to bypass filters -> {red}")
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} {replacechar(msg)}")