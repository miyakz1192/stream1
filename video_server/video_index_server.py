#!/usr/bin/env python3
import os
import requests
from pathlib import Path
from flask import *
from consts import *



app = Flask(__name__)

# config area
TOKEN_CHECK_URL="http://127.0.0.1:8000/check"
VIDEO_DIR="./video"

def has_valid_token():
    print("INFO: token check: start")
    user_info = request.cookies.get(COKKIE_ALL_NAME)
    if user_info is None:
        return False 

    print("INFO: token check: get json")
    user_info = json.loads(user_info)

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
    

class FileRank:
    def sort_top(self, findex):
        return findex

    def up(self, file_name):
        return

class FileIndex:
    def __init__(self):
        # ディレクトリパス
        directory_path = Path(VIDEO_DIR)
        # ディレクトリ内のファイル一覧を取得
        files = directory_path.glob('*')
        # ファイル名のみのリストを作成
        file_names_only = [file.name for file in files if file.is_file()]
        self.index = file_names_only



@app.route("/")
def get_file_list():
    print("INFO: CH")
    if has_valid_token() is False:
        return "NG"

    findex = FileIndex()
    return render_template('index.html', file_names=findex.index)

@app.route("/<file_name>")
def forward_to_video_server():
    if has_valid_token() is False:
        return "NG"

    return redirect('https://example.com')


if __name__ == "__main__":
    app.run("0.0.0.0", port=8001, debug=True)
