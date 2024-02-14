
import requests
from flask import *
from consts import *
import http.cookies


TOKEN_CHECK_URL="http://127.0.0.1:8000/check"

def has_valid_token(using_mw="flask", self=None):

    if using_mw == "flask":
        print("INFO: token check: start")
        user_info = request.cookies.get(COKKIE_ALL_NAME)
        if user_info is None:
            return False 
    
        print("INFO: token check: get json")
        user_info = json.loads(user_info)
    elif using_mw == "simple":
        cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))
        if COKKIE_ALL_NAME in cookies:
            user_info = json.loads(cookies[COKKIE_ALL_NAME].value)

    token = user_info[COKKIE_TOKEN_NAME] 
    print(f"INFO: token check: get token target token={token}")

    if token is None:
        return False 

    print("INFO: token check: to server")

    try:
        params = {COKKIE_TOKEN_NAME: token}
        res = requests.get(TOKEN_CHECK_URL, params=params)
    except:
        print("INFO: token check: some error(may be net)")
        return False

    if res.text is None:
        print("INFO: token check: text is none")
        return False

    print(f"INFO: token check: text is {res.text}")

    if res.text == "OK":
        return True

    return False
