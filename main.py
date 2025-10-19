import asyncio, time, os, inspect, types
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

modnum = len(modules)

class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    WHITE = "\033[97m"

choices = [str(i) for i in range(1, modnum + 1)]

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
    print(f"{red}{ascii_art}{red}")
    for m in modules:
        print(f"{white}{m.module_number}. {m.__name__.split('.')[-1]}{red}")

    while True:
        uchoice = input(f"{BEFORE}{current_time_hour()}{AFTER} {INPUT} Enter function ({choices} or 'q' to quit) -> {red}").strip().lower()
        if uchoice == 'q':
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ADD} Exiting program.")
            break
        try:
            choice = int(uchoice)
        except ValueError:
            Error(f"Invalid input. Please enter {choices} or 'q'.")
            continue
        if choice not in range(1, modnum + 1):
            Error(f"Invalid choice. Please enter {choices} or 'q'.")
            continue
        selected_module = next((m for m in modules if m.module_number == choice), None)
        if not selected_module:
            Error("Selected module not found.")
            continue
        for attr_name in dir(selected_module):
            if attr_name.startswith("_"):
                continue
            attr = getattr(selected_module, attr_name)
            if isinstance(attr, types.FunctionType) or asyncio.iscoroutinefunction(attr):
                try:
                    sig = inspect.signature(attr)
                    if len(sig.parameters) == 0:
                        if asyncio.iscoroutinefunction(attr):
                            await attr()
                        else:
                            attr()
                except (ValueError, TypeError):
                    continue

if __name__ == '__main__':
    asyncio.run(main())
