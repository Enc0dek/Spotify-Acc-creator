from spotify import Spotify
import utils
import console
from colorama import Fore
from time import sleep
import os

FILE_PATH = "./accs.txt"
cls = console.Console("Spotify acc gen")
MAGENTA = Fore.MAGENTA
RESET = Fore.RESET

URLS = {
    "SIGN_UP": "https://www.spotify.com/us/signup"
}
EXTENSIONS = ["./anticaptcha.crx"]

def main():
    accs = []
    cls.best_print(f"{MAGENTA} BY LZ000 {RESET} \n")
    
    username = cls.input_user("Username: ", crisp=True)
    password = cls.input_user("Password: ", crisp=True)
    num_accs = int(cls.input_user("Num Accs: ", crisp=True))
    
    emails = utils.get_mails(num_accs)
    sp = Spotify(extensions_path=EXTENSIONS, debug=True)
    
    for email in emails:
        sp.get(URLS["SIGN_UP"])
        
        sp.create_account(email, password, username)
        
        acc = f"{email}:{password}"
        
        cls.success(f"{acc}")
        accs.append(acc)
        sp.reset()
        
    if os.path.exists(FILE_PATH):
        data = utils.read_file(FILE_PATH)
        
        for acc in accs:
            data.append(acc)
            
        utils.write_file(FILE_PATH, data)
    else:
        utils.write_file(FILE_PATH, accs)

if __name__ == "__main__":
    main()