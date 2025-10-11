import asyncio,time
from datetime import datetime
from utils.userlookup import username_finder
from utils.phonelookup import numlookup
from utils.ipping import ipping
from utils.ipscanner import ipscan
from utils.emaillookup import emaillookup
from utils.unamedorksearch import unamedorksearch
from utils.emaildorksearch import emaildorksearch
class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    WHITE = "\033[97m"

choices = ['1', '2', '3', '4','5','6','7']

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



ascii_art=('''
 ██▒   █▓ ▒█████   ██  █████▄    ▄▄▄█████▓ ██▀███   ▄▄▄       ▄████▄  ▓█████ 
▓██░   █▒▒██▒  ██▒▓  ▒▒██▀ ██▌   ▓  ██▒ ▓▒▓██ ▒ ██▒▒████▄    ▒██▀ ▀█  ▓█   ▀ 
 ▓██  █▒░▒██░  ██▒▒██▒░██   █▌   ▒ ▓██░ ▒░▓██ ░▄█ ▒▒██  ▀█▄  ▒▓█    ▄ ▒███   
  ▒██ █░░▒██   ██░░██░░▓█▄   ▌   ░ ▓██▓ ░ ▒██▀▀█▄  ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▒▓█  ▄ 
   ▒▀█░  ░ ████▓▒░░██░░█████▓      ▒██▒ ░ ░██▓ ▒██▒ ▓█   ▓██▒▒ ▓███▀ ░░▒████▒
   ░ ▐░  ░ ▒░▒░▒░ ░▓   ▒▒▓  ▒      ▒ ░░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ░▒ ▒  ░░░ ▒░ ░
   ░ ░░    ░ ▒ ▒░  ▒ ░ ░ ▒  ▒        ░      ░▒ ░ ▒░  ▒   ▒▒ ░  ░  ▒    ░ ░  ░
     ░░  ░ ░ ░ ▒   ▒ ░ ░ ░  ░      ░        ░░   ░   ░   ▒   ░           ░   
      ░      ░ ░   ░     ░                   ░           ░  ░░ ░         ░  ░
     ░                 ░                                     ░               
'''
)
def main():

    print(f"{red }{ascii_art}{red}")
    print(f"{white}1. User lookup\n2. Phone lookup\n3. IP ping\n4. IP scanner\n5. Email lookup\n6. Username dorksearch\n7. Email dorksearch{red}")

    while True:
        uchoice = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Enter function ({choices} or 'q' to quit) -> {red}").strip().lower()
        if uchoice == 'q':
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Exiting program.")
            break
        if uchoice not in choices:
            Error(f"Invalid choice. Please enter {choices} or 'q'.")
            continue
        if uchoice == '1': asyncio.run(username_finder())
        elif uchoice == '2': numlookup()
        elif uchoice == '3': ipping()
        elif uchoice == '4': ipscan()
        elif uchoice == '5': emaillookup()
        elif uchoice == "6": unamedorksearch()
        elif uchoice == "7": emaildorksearch()
if __name__ == '__main__':
    main()