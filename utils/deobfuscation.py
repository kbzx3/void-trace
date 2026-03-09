import base64
import binascii
import time
from datetime import datetime

class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
module_display_name = "String Deobfuscation"
description = '''
Description:
A string-processing module implementing base64 decoding, hexadecimal byte-conversion, and 
urllib.parse for percent-decoding. It also features a manual Caesar cipher 
implementation for ROT13 and a slicing-based string reversal method.

Usage:
1. Select a method by typing a number from 1 to 5 (e.g., 1 for Base64).
2. Paste the scrambled or encoded text when prompted.
3. The tool will process the input and display the "Decoded" original message.
'''
white = Color.WHITE
red = Color.RED
green = Color.GREEN
yellow = Color.YELLOW
color = Color()

BEFORE = "["
AFTER = "]"
ADD = "[+]"
ERROR = "[!]"
INPUT = "[?]"
SUCCESS = "[✓]"

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Slow(text, delay=0.05):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def Error(message):
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} {red}{message}{Color.RESET}")

def Success(message):
    print(f"{BEFORE}{current_time_hour()}{AFTER} {SUCCESS} {green}{message}{Color.RESET}")

def Info(message):
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} {white}{message}{Color.RESET}")

deobf_banner = """
==============================================
     DEOBFUSCATION TOOLKIT v1.0
==============================================
"""

def deobfuscate_base64(data):
    try:
        decoded = base64.b64decode(data).decode('utf-8')
        return True, decoded
    except Exception as e:
        return False, f"Invalid Base64: {str(e)}"

def deobfuscate_hex(data):
    try:
        cleaned = data.replace(" ", "").replace("0x", "").replace("\\x", "")
        decoded = bytes.fromhex(cleaned).decode('utf-8')
        return True, decoded
    except Exception as e:
        return False, f"Invalid Hex: {str(e)}"

def deobfuscate_url(data):
    try:
        import urllib.parse
        decoded = urllib.parse.unquote(data)
        if decoded == data:
            return False, "No URL encoding detected"
        return True, decoded
    except Exception as e:
        return False, f"Invalid URL encoding: {str(e)}"

def deobfuscate_rot13(data):
    try:
        decoded = ""
        for char in data:
            if 'a' <= char <= 'z':
                decoded += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                decoded += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
            else:
                decoded += char
        return True, decoded
    except Exception as e:
        return False, f"Invalid ROT13: {str(e)}"

def deobfuscate_reverse(data):
    try:
        decoded = data[::-1]
        return True, decoded
    except Exception as e:
        return False, f"Error reversing string: {str(e)}"

def deobfuscation():
    Slow(deobf_banner, delay=0.01)
    
    methods = {
        "1": ("Base64", deobfuscate_base64),
        "2": ("Hexadecimal", deobfuscate_hex),
        "3": ("URL Encoding", deobfuscate_url),
        "4": ("ROT13", deobfuscate_rot13),
        "5": ("String Reversal", deobfuscate_reverse)
    }
    
    print(f"\n{red}╔══════════════════════════════════════╗{Color.RESET}")
    print(f"{red}║  {white}Available Deobfuscation Methods{red}    ║{Color.RESET}")
    print(f"{red}╠══════════════════════════════════════╣{Color.RESET}")
    print(f"{red}║  {white}[1] Base64 Decoding{red}                ║{Color.RESET}")
    print(f"{red}║  {white}[2] Hexadecimal Decoding{red}           ║{Color.RESET}")
    print(f"{red}║  {white}[3] URL Decoding{red}                   ║{Color.RESET}")
    print(f"{red}║  {white}[4] ROT13 Cipher{red}                   ║{Color.RESET}")
    print(f"{red}║  {white}[5] String Reversal{red}                ║{Color.RESET}")
    print(f"{red}╚══════════════════════════════════════╝{Color.RESET}\n")
    
    while True:
        choice = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Select method (1-5 or 'q' to return to menu) -> {Color.RESET}").strip().lower()
        
        if choice == 'q':
            Info("Returning to menu.")
            return
        
        if choice not in methods:
            Error("Invalid choice! Please select 1-5.")
            continue
        
        method_name, method_func = methods[choice]
        Info(f"Selected method: {yellow}{method_name}{Color.RESET}")
        break
    
    obfuscated_input = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Enter obfuscated string -> {Color.RESET}").strip()
    
    if not obfuscated_input:
        Error("Empty input! Returning to menu.")
        return
    
    Info(f"Processing with {yellow}{method_name}{Color.RESET}...")
    time.sleep(0.3)
    
    is_valid, result = method_func(obfuscated_input)
    
    print(f"\n{red}{'='*50}{Color.RESET}")
    if is_valid:
        Success(f"Valid {method_name} detected!")
        print(f"{BEFORE}{current_time_hour()}{AFTER} {white}Original:{Color.RESET} {yellow}{obfuscated_input[:100]}{'...' if len(obfuscated_input) > 100 else ''}{Color.RESET}")
        print(f"{BEFORE}{current_time_hour()}{AFTER} {white}Decoded:{Color.RESET}  {green}{result}{Color.RESET}")
    else:
        Error(f"Deobfuscation failed!")
        print(f"{BEFORE}{current_time_hour()}{AFTER} {white}Reason:{Color.RESET} {red}{result}{Color.RESET}")
    print(f"{red}{'='*50}{Color.RESET}\n")