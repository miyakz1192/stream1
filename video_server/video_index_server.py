#!/usr/bin/env python3
import os
import requests
from pathlib import Path
from flask import *
from consts import *
from stream_sv_lib import *


app = Flask(__name__)

# config area
VIDEO_DIR="./video"

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

@app.route("/goto/<string:file>/")
def forward_to_video_server(file):
    if has_valid_token() is False:
        return "NG"

    temp = f"<video controls width='100%' height='auto'><source src='./video/{file}'> </video>"
    with open("index.html", "w") as f:
        f.write(temp)

    return redirect('http://192.168.122.195:8080/index.html')


if __name__ == "__main__":
    app.run("0.0.0.0", port=8001, debug=True)
