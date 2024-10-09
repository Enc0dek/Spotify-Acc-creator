from colorama import Fore
from colorama.ansi import AnsiFore
import datetime
from time import sleep
from os import system

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
RESET = Fore.RESET

class Console:
    def __init__(self, timestamps: bool = False, Console_title = None) -> None:
        self.timestamps = timestamps
        self.console_title = Console_title
        
        if self.console_title:
            self.update_console_title(self.console_title)
        
    def get_timestamp(self) -> str:
        current_timestamp = datetime.datetime.now()
        
        return current_timestamp.strftime("%H:%M:%S")
        
    def warning(self, *values: str):
        timestamp = None
        message = "".join(values)
        
        if self.timestamps:
            timestamp = self.get_timestamp()
        
        if timestamp != None:
            print(f"{YELLOW} {timestamp} [WARNING] > {message} {RESET}")
        else:
            print(f"{YELLOW} [WARNING] > {message} {RESET}")
            
    def info(self, *values: str):
        timestamp = None
        message = "".join(values)
        
        if self.timestamps:
            timestamp = self.get_timestamp()
        
        if timestamp != None:
            print(f"{BLUE} {timestamp} [INFO] > {message} {RESET}")
        else:
            print(f"{BLUE} [INFO] > {message} {RESET}")
            
    def error(self, *values: str):
        timestamp = None
        message = "".join(values)
        
        if self.timestamps:
            timestamp = self.get_timestamp()
        
        if timestamp != None:
            print(f"{RED} {timestamp} [ERROR] > {message} {RESET}")
        else:
            print(f"{RED} [ERROR] > {message} {RESET}")
            
    def success(self, *values: str):
        timestamp = None
        message = "".join(values)
        
        if self.timestamps:
            timestamp = self.get_timestamp()
        
        if timestamp != None:
            print(f"{GREEN} {timestamp} [!] > {message} {RESET}")
        else:
            print(f"{GREEN} [!] > {message} {RESET}")
            
    def best_print(self, *values: str, timeout: float = 0.1):
        message = "".join(values)
        
        for char in message:
            print(char, end="", flush=True)
            sleep(timeout)
    
    def input_user(self, *values, color: AnsiFore = None, crisp: bool = False, timeout: float = 0.1):

        msg = "".join(values)
        if color:
            msg = f"{color}{msg}{RESET}"
        
        if crisp:
            self.best_print(msg, timeout=timeout)
        else:
            print(msg)

        return input()
    
    def update_console_title(self, *values):
        title = "".join(values)
        system(f"title {title}")