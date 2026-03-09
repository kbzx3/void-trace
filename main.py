import asyncio, time, os, inspect, types, sys, re
from datetime import datetime

modules = []
folder = os.path.join(os.path.dirname(__file__), 'utils')
for file in os.listdir(folder):
    if file.endswith('.py') and file != "__init__.py":
        modulename = file[:-3]
        module = __import__(f'utils.{modulename}', fromlist=[modulename])
        modules.append(module)

for index, module in enumerate(modules, start=1):
    module.module_number = index
def printmodulenames():
    for m in modules:
        display_name = getattr(m, 'module_display_name', m.__name__.split('.')[-1])
        print(f"{white}{m.module_number}. {display_name}{white}")
modnum = len(modules)
def cls():
    if os.name == "nt": os.system('cls')
    else: os.system('clear')
class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    WHITE = "\033[97m"
class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        if not filename.lower().endswith('.txt'):
            filename += '.txt'
        self.log = open(filename, "a", encoding="utf-8")
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def write(self, message):
        self.terminal.write(message)
        clean_message = self.ansi_escape.sub('', message)
        self.log.write(clean_message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

choices = f"1-{modnum}"

white = Color.WHITE
red = Color.RED

BEFORE = "["
AFTER = "]"
ADD = "[+]"
ERROR = "[!]"
INPUT = "[?]"

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Slow(text, delay=0.01):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def Error(message):
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} {message}")
miscinfo = '''
Description:
Void Trace is a modernized open-source intelligence (OSINT) and reconnaissance tool built in Python. 
It serves as a modular framework for analyzing phone numbers, web metadata, and network layers 
through a terminal-driven interface. The system uses a dynamic module loader in 
main.py that automatically detects and imports utility scripts from the utils/ folder.

How to Develop Addons:
1. File Creation: Create a new .py file and place it specifically inside the 'utils' folder.
2. Function Naming: You MUST define a main function inside your script that has the exact same 
   name as the file itself (e.g., 'tools.py' must have 'def tools():').
3. Parameters: The entry function must take zero arguments to be compatible with the 
   automatic caller in main.py.
4. Metadata: At the top of your script, include 'module_display_name' for the menu title 
   and 'description' for the help text.

Usage & FAQ:
- Restart Required: After adding or removing a tool via the Addon Manager, you must restart 
  the program to refresh the menu.
- Navigation: Use the numbers 1-10 to select tools, 'h' for help info, and 'q' to quit.
- Formatting: For phone tools, always use the '+' prefix with the country code.
- Safety: If a tool shows [WAIT], do not interrupt the process as it is fetching live 
  data from external APIs or websites.
'''
def help():
    try:
        printmodulenames()
        helpmodnum_=input(f"{INPUT} Enter function number ({choices}) or 'm' for miscellaneous info: {white}")
        if helpmodnum_ == 'm':
            print(f"{ADD} {miscinfo}")
        elif int(helpmodnum_) in range(10):
            helpmodnum = int(helpmodnum_)
            helpmodule = modules[helpmodnum-1]
            helpinfo=getattr(helpmodule,"description", "No help info found")
            print(f" {ADD} {helpinfo} {white}")
        else: print(f"{red} {ERROR} Invalid input {red}")
    except Exception as e: print(f"{ERROR} {e}")
ascii_art = '''
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

async def main():
    logging_enabled = False
    asked_for_logging = False
    while True:
        output = sys.stdout.terminal if isinstance(sys.stdout, Logger) else sys.stdout
        output.write(f"{red}{ascii_art}{red}")
        output.flush()
        if isinstance(sys.stdout, Logger):
            original_stdout = sys.stdout
            sys.stdout = sys.stdout.terminal
        Slow(f"\n{red}╔══════════════════════════════════════╗{Color.RESET}")        
        for m in modules:
            display_name = getattr(m, 'module_display_name', m.__name__.split('.')[-1])
            Slow(f"║{white}{m.module_number}. {display_name}{red}")
        Slow(f"{red}╚══════════════════════════════════════╝{Color.RESET}\n")
        if isinstance(sys.stdout, Logger):
            sys.stdout = original_stdout
        else:
            original_stdout = None
        if isinstance(sys.stdout, Logger):
            sys.stdout.log.write("[banner + module list]\n")
        if not asked_for_logging:
            log_choice = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Enable session logging? (y/n) -> {red}").strip().lower()
            if log_choice == 'y':
                file_name = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Enter filename for this log (e.g., session1) -> {red}").strip()
                if not file_name:
                    file_name = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                sys.stdout = Logger(file_name)
                print(f"\n--- Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
                logging_enabled = True
            asked_for_logging = True
        uchoice = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Enter function ({choices}, 'h' for info/help or 'q' to quit) -> {red}").strip().lower()
        if isinstance(sys.stdout, Logger):
            print(f"User Input: {uchoice}")
        cls()
        if uchoice == 'q':
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Exiting program.")
            break
        elif uchoice == 'h':
            help()
            continue
        try:
            choice = int(uchoice)
        except ValueError:
            Error(f"Invalid input. Please enter {choices},h or 'q'.")
            continue
        
        if choice not in range(1, modnum + 1):
            Error(f"Invalid choice. Please enter {choices},h or 'q'.")
            continue
        selected_module = next((m for m in modules if m.module_number == choice), None)
        if not selected_module:
            Error("Selected module not found.")
            continue
        module_name = selected_module.__name__.split('.')[-1]
        attr = getattr(selected_module, module_name, None)
        if not attr:
            Error(f"Function '{module_name}()' not found in module.")
            continue
        if isinstance(attr, types.FunctionType) or inspect.iscoroutinefunction(attr):
            try:
                sig = inspect.signature(attr)
                if len(sig.parameters) == 0:
                    cls()
                    if inspect.iscoroutinefunction(attr):
                        await attr()
                    else:
                        attr()
                else:
                    Error(f"Function '{module_name}()' requires parameters.")
            except (ValueError, TypeError) as e:
                Error(f"Could not execute '{module_name}()': {str(e)}")
        else:
            Error(f"'{module_name}' is not a callable function.")

if __name__ == '__main__':
    asyncio.run(main())