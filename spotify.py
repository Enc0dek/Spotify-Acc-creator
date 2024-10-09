from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import utils
import console
from time import sleep

cls = console.Console(True)

FINAL_URL = "https://www.spotify.com/us/download/windows/"

ELEMENTS = {
    "email_input": (By.ID , "username"),
    "next_button": (By.XPATH, "//button[contains(@class, 'Button-sc-qlcn5g-0') and contains(@class, 'VsdHm')]//span[contains(@class, 'ButtonInner-sc-14ud5tc-0') and text()='Next']"),
    "password_input": (By.XPATH, "//input[@id='new-password' and @type='password' and @aria-invalid='false' and @autocomplete='new-password']"),
    "username_input": (By.XPATH, "//input[@id='displayName' and @type='text' and @aria-invalid='false' and @autocomplete='given-name']"),
    "day_input": (By.XPATH, "//input[@id='day' and @type='numeric' and @maxlength='2' and @autocomplete='bday-day' and @placeholder='dd']"),
    "month_input": (By.XPATH, "//select[@id='month' and @name='month' and @autocomplete='bday-month' and @data-testid='birthDateMonth']"),
    "year_input": (By.XPATH, "//input[@id='year' and @type='numeric' and @maxlength='4' and @autocomplete='bday-year' and @placeholder='yyyy']"),
    "gender_input": (By.XPATH, "//label[@for='gender_option_male']//span[text()='Man']"),
    "signin_button": (By.XPATH, "//button[@data-testid='submit' and @data-encore-id='buttonPrimary' and contains(., 'Sign up')]"),
    "captcha_next_button": (By.XPATH, "//button[@data-is-ready='true' and @name='solve' and @data-encore-id='buttonPrimary' and contains(@class, 'Button-sc-qlcn5g-0') and contains(@class, 'hRpqrX')]//span[contains(@class, 'ButtonInner-sc-14ud5tc-0') and contains(@class, 'hCjoKJ') and text()='Continue']"),
    "captha_page": (By.XPATH, "//h1[contains(@class, 'Type__TypeElement-sc-goli3j-0') and contains(@class, 'gcUwpS') and contains(@class, 'sc-kLhKbu') and contains(@class, 'ctPRtA') and text()='We need to make sure that you\'re a human']")
}

POPUPS = ["onetrust-banner-sdk"]

def get_element(driver: WebDriver, type:By, element:str, timeout:int = 10) -> WebElement:
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((type, element)))
    except:
        cls.error(f"Finding By: {type}, Element {element}")
        exit(1)

def select_value(element: WebElement, value):
    select_element = Select(element)
    select_element.select_by_value(str(value))

class Spotify:
    def __init__(self, extensions_path: list = [], debug: bool = False) -> None:
        self.debug = debug
        self.options = webdriver.ChromeOptions()
        self.extensions_path = extensions_path
        
        if len(self.extensions_path) >= 1:
            for ext in self.extensions_path:
                self.options.add_extension(ext)
                
                if self.debug:
                    cls.info(f"Extension Loaded {ext}")
            
        self.driver = webdriver.Chrome(options=self.options)
    
    def get(self, url: str):
        self.driver.get(url)

        if self.debug:
            cls.info(f"REDIRECTING TO {url}")
        
    def next(self):
        get_element(self.driver, ELEMENTS["next_button"][0], ELEMENTS["next_button"][1]).click()
        
    def next_captcha(self):
        current_url = self.driver.current_url
        try:
            get_element(self.driver, ELEMENTS["captcha_next_button"][0], ELEMENTS["captcha_next_button"][1]).click()
            
            while current_url != FINAL_URL:
                get_element(self.driver, ELEMENTS["captcha_next_button"][0], ELEMENTS["captcha_next_button"][1]).click()
                sleep(0.3)
        except:
            pass
        
    
    def detect_captcha(self) -> bool:
        cls.info("Searching captcha page")
        try: 
            page = get_element(self.driver, ELEMENTS["captha_page"][0],ELEMENTS["captha_page"][1])
            
            while not page:
                page = get_element(self.driver, ELEMENTS["captha_page"][0],ELEMENTS["captha_page"][1])
                
        except:
            pass
    
        return True
    
    def do_captcha(self):
        self.driver.execute_script(r"document.body.appendChild(Object.assign(document.createElement('iframe'), { src: 'chrome-extension://hlifkpholllijblknnmbfagnkjneagid/popup/popup.html#/' }));")
        
    def create_account(self, email: str, password: str, username: str):
        self.hide_popups(POPUPS)
        date = utils.gen_date()
        
        day = date["day"]
        month = date["month"]
        year = date["year"]
        
        email_input = get_element(self.driver, ELEMENTS["email_input"][0], ELEMENTS["email_input"][1])
        email_input.send_keys(email)
        sleep(0.5)
        
        self.next()
        
        password_input = get_element(self.driver, ELEMENTS["password_input"][0], ELEMENTS["password_input"][1])
        password_input.send_keys(password)
        sleep(0.5)
        
        self.next()
        
        username_input = get_element(self.driver, ELEMENTS["username_input"][0], ELEMENTS["username_input"][1])
        day_input = get_element(self.driver, ELEMENTS["day_input"][0], ELEMENTS["day_input"][1])
        month_input = get_element(self.driver, ELEMENTS["month_input"][0], ELEMENTS["month_input"][1])
        year_input = get_element(self.driver, ELEMENTS["year_input"][0], ELEMENTS["year_input"][1])
        gender_input = get_element(self.driver, ELEMENTS["gender_input"][0], ELEMENTS["gender_input"][1])
        
        username_input.send_keys(username)
        day_input.send_keys(day)
        select_value(month_input, month)
        year_input.send_keys(year)  
        gender_input.click()
        sleep(0.5)
        
        self.next()
        
        get_element(self.driver, ELEMENTS["signin_button"][0], ELEMENTS["signin_button"][1]).click()
        sleep(1)
    
        if self.detect_captcha():
            if self.debug:
                cls.info("Captcha page Founded")
            self.do_captcha()
        self.next_captcha()
        
        
    def hide_popups(self, popups):
        for popup in popups:
            try:
                self.driver.execute_script(f'document.getElementById("{popup}").style.display = "None"')
            
                if self.debug:
                    cls.info(f"Element hiden {popup}")
            except:
               pass
           
               if self.debug:
                    cls.error(f"HIDING {popup}")

    def reset(self):
        self.driver.delete_all_cookies()
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")
        self.driver.refresh()
        
        if self.debug:
            cls.warning("ALL DATA DELETED")
        
