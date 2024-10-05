from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import random
import time
import requests
import sys
from tempmail import EMail
from colorama import Fore
import os.path as path

URL = "https://www.spotify.com/mx/signup?forward_url=https%3A%2F%2Fopen.spotify.com%2F"
DELAY_BYPASS = 0.15

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
PURPLE = Fore.MAGENTA
RESET = Fore.RESET

FILE_PATH = "./accs.txt"

ELEMENTS = {
    "email_input": (By.ID , "username"),
    "next_button": (By.XPATH, '//button[@data-testid="submit" and @data-encore-id="buttonPrimary"]//span[text()="Next"]'),
    "password_input": (By.XPATH, "//input[@id='new-password' and @type='password' and @aria-invalid='false' and @autocomplete='new-password']"),
    "username_input": (By.XPATH, "//input[@id='displayName' and @type='text' and @aria-invalid='false' and @autocomplete='given-name']"),
    "day_input": (By.XPATH, "//input[@id='day' and @type='numeric' and @maxlength='2' and @autocomplete='bday-day' and @placeholder='dd']"),
    "month_input": (By.XPATH, "//select[@id='month' and @name='month' and @autocomplete='bday-month' and @data-testid='birthDateMonth']"),
    "year_input": (By.XPATH, "//input[@id='year' and @type='numeric' and @maxlength='4' and @autocomplete='bday-year' and @placeholder='yyyy']"),
    "gender_input": (By.XPATH, "//label[@for='gender_option_male']//span[text()='Man']"),
    "signin_button": (By.XPATH, "//button[@data-testid='submit' and @data-encore-id='buttonPrimary' and contains(., 'Sign up')]")
}

def get_element(driver: WebDriver, type: By, element: str, timeout: int = 10) -> WebElement:
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((type, element)))

class Spotify:
    def __init__(self, url) -> None:
        self.url = url
        self.date = {"day": random.randint(1,29), "month": random.randint(1,12), "year": random.randint(1990, 2000)}
        self.driver = webdriver.Firefox() # change this line for your browser
        
        self.driver.get(self.url)

    def next(self):
        get_element(self.driver, ELEMENTS["next_button"][0], ELEMENTS["next_button"][1]).click()


    def register(self, email: str, password: str, username: str) -> bool:
        if validate_email(email) and validate_password(password):
            # set email
            email_input = get_element(self.driver, ELEMENTS["email_input"][0], ELEMENTS["email_input"][1])
            bypass_write(email_input, email, DELAY_BYPASS)
            time.sleep(0.5)
            self.next()
            
            time.sleep(0.3)

            # set password

            password_input = get_element(self.driver, ELEMENTS["password_input"][0], ELEMENTS["password_input"][1])
            bypass_write(password_input, password, DELAY_BYPASS)
            time.sleep(0.3)
            self.next()

            time.sleep(0.3)

            # set details

            username_input = get_element(self.driver, ELEMENTS["username_input"][0], ELEMENTS["username_input"][1])

            day_input = get_element(self.driver, ELEMENTS["day_input"][0], ELEMENTS["day_input"][1])
            month_input = get_element(self.driver, ELEMENTS["month_input"][0], ELEMENTS["month_input"][1])
            year_input = get_element(self.driver, ELEMENTS["year_input"][0], ELEMENTS["year_input"][1])

            gender_input = get_element(self.driver, ELEMENTS["gender_input"][0], ELEMENTS["gender_input"][1])

            bypass_write(username_input, username, DELAY_BYPASS)
            bypass_write(day_input, self.date["day"], DELAY_BYPASS)
            bypass_write(year_input, self.date["year"], DELAY_BYPASS)
            select_value(month_input, self.date["month"])
            

            gender_input.click()
            time.sleep(0.3)
            self.next()
            
            time.sleep(0.5)
            self.url = self.driver.current_url
            get_element(self.driver, ELEMENTS["signin_button"][0], ELEMENTS["signin_button"][1]).click()
            

            try:
                WebDriverWait(self.driver, 10).until(lambda d: d.current_url != self.url)
                return 0
            except:
                return 1
        else:
            print(F"{RED}[!] Invalid email or password {RESET}")
            return 1
    def exit(self):
        self.driver.close()

def select_value(element: webdriver, value):
    select_element = Select(element)
    select_element.select_by_value(str(value))

def bypass_write(element: WebElement, text: str, timeout = 0.2):
    for char in str(text):
        element.send_keys(char)
        time.sleep(timeout)

def validate_email(email: str) -> bool:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br"
    }

    try:
        r = requests.get(f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={email}", headers=headers)

        if r.status_code == requests.codes.ok:
            json = r.json()

            if json["status"] == 1:
                return True
            else:
                return False
    except TimeoutError:
        print(F"{RED}[!] timeout ERROR {RESET}")

def validate_password(password: str) -> bool:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br"
    }
    try:
        r = requests.get(f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&password={password}", headers=headers)

        if r.status_code == requests.codes.ok:
            json = r.json()
            if json["status"] != 100:
                return True
            else:
                return False
    except TimeoutError:
        print(F"{RED}[!] timeout ERROR")
        sys.exit(1)

def get_mail() -> str:
    try:
        email = EMail()
        return email.address
    except:
        print(f"{RED} [!] UNABLE TO GET TEMP EMAIL {RESET}")

def read_file(file) -> list:
    with open(file, "r", encoding='utf-8') as f:
        return f.readlines()
    
def write_file(file, data):
    with open(file, "w", encoding='utf-8') as f:
        f.writelines(data)

def main():
    mails = []
    accs = []
    print(f"{PURPLE} BY LZ000 {RESET}")

    username = input("Acc username: ")
    password = str(input("Acc password: "))
    num_accs = int(input("Number of Accs: "))

    for _ in range(num_accs):
        mails.append(get_mail())

    for mail in mails:
        sp = Spotify(URL)
        if sp.register(mail, password, username) == 0:
            acc = f"{mail}:{password}"
            accs.append(acc)
            print(f"{GREEN} [!] Account created: {acc} {RESET}")
        sp.exit()


    if path.exists(FILE_PATH):
        data = read_file(FILE_PATH)

        for acc in accs:
            data.append(acc)

        write_file(FILE_PATH, data)
    else:
        write_file(FILE_PATH, accs)

if __name__ == "__main__":
    main()