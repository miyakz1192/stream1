#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
import uuid
from flask import *
import pickle
from consts import *

app = Flask(__name__)

# reference page
# cookie ussage
# https://qiita.com/tani_exe/items/6297ad0fede4da72173c


class TokenData:
    TOKEN_FILE_NAME = "./tokendata.pickle"
    def __init__(self):
        self.expire = 60 * 60 * 4 #seconds (4 hour)
        # self.expire = 30  #seconds
        self.refresh_now()

    @classmethod
    def load_from_file(cls):
        try:
            with open(TokenData.TOKEN_FILE_NAME, "rb") as f:
                print("INFO: read token from file")
                loaded_obj = pickle.load(f)
            return loaded_obj
        except: 
            print("INFO: file not found or some error, generate now token")
            return TokenData()

    @classmethod
    def save_to_file(cls, target):
        print(f"INFO: save token , {target.start_date}")
        with open(TokenData.TOKEN_FILE_NAME, "wb") as f:
            pickle.dump(target, f)

    def save(self):
        TokenData.save_to_file(self)

    def is_expired(self):
        now = datetime.now()
        print(f"INFO: {self.start_date}")
        print(f"INFO: {self.start_date+timedelta(seconds=self.expire)}")
        print(f"INFO: {now}")
        if self.start_date + timedelta(seconds=self.expire) < now:
            print("INFO: token is expired")
            return True

        print("INFO: token is NOT expired")
        return False

    def refresh_now(self):
        self.token = str(uuid.uuid4())
        self.start_date = datetime.now()

@app.route("/get_token/", methods=["POST"])
def get_token():
    # TODO: check otp
    indata = request.form['indata']
    max_age = 60 * 60 * 24 # one day 
    expires = int(datetime.now().timestamp()) + max_age
    response = make_response(f"get token in your cokkie! {indata}")
    new_token = TokenData()
    user_info = {'token':new_token.token}
    new_token.save()
    response.set_cookie(COKKIE_SITE_NAME, 
                        value=json.dumps(user_info), expires=expires)
    return response

@app.route('/')
def form():
    return render_template('./index.html')

@app.route("/check/")
def check():
    user_info = request.cookies.get(COKKIE_SITE_NAME)
    if user_info is not None:
        user_info = json.loads(user_info)

    local_saved_token = TokenData.load_from_file()

    if local_saved_token.token != user_info["token"]:
        print(f"INFO: {local_saved_token.token} != {user_info['token']}")
        return "NG"

    print(f"INFO: {local_saved_token.token} == {user_info['token']}")
    if local_saved_token.is_expired():
        return "NG"

    return "OK"

def create_token():
    pass

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000, debug=True)
