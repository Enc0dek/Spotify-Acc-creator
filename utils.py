import httpx
from httpx import Client
import console
from sys import exit
from colorama import Fore
from tempmail import EMail
from random import randint

YELLOW = Fore.YELLOW
cls = console.Console(True)

def validate_email(client: Client, email: str):
    url = f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={email}"
    
    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br"
    }

    try:
        r = client.get(url=url, headers=headers)

        if r.status_code == httpx.codes.ok:
            json = r.json()

            if json["status"] == 1:
                return 0
            else:
                return 1
    except TimeoutError:
        cls.error(f"Timeout {YELLOW} >[SAVING INFO]<")
        return 2

def validate_password(client: Client, password: str) -> bool:
    url = f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&password={password}"
    
    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br"
    }
    try:
        r = client.get(url=url, headers=headers)

        if r.status_code == httpx.codes.ok:
            json = r.json()
            if json["status"] != 100:
                return True
            else:
                cls.error(f"Invalid Passowrd: {password}")
                return False
    except httpx.TimeoutException:
        cls.error("Timeout")
        exit(1)
    
    except httpx.RequestError as exc:
        cls.error(f"Error in Request: {exc}")
        exit(1)

def read_file(file) -> list:
    with open(file, "r", encoding='utf-8') as f:
        return f.readlines()
    
def write_file(file, data):
    with open(file, "w", encoding='utf-8') as f:
        f.writelines(data)
        
def get_mail() -> str:
    try:
        return EMail().address
    except:
        cls.error("UNABLE TO GET TEMP EMAIL")
        
def get_mails(num: int) -> list:
    mails = []
    
    for _ in range(num):
        mails.append(get_mail())
        
    return mails
        
def gen_date() -> dict:
    day = randint(1,28)
    month = randint(1,12)
    year = randint(1990,2000)
    
    return {"day": day, "month": month, "year": year}
    