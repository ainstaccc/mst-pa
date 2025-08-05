import os
import json
from flask import Flask, render_template
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# --------------------------
# 讀取 Render 環境變數中的金鑰
# --------------------------
google_creds_json = os.environ.get("GCP_CREDENTIALS")
creds_dict = json.loads(google_creds_json)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
gc = gspread.authorize(creds)

# --------------------------
# Flask 首頁
# --------------------------
@app.route("/")
def index():
    return render_template("index.html")

# --------------------------
# 讀取 Google Sheet 資料
# --------------------------
@app.route("/data")
def get_data():
    sheet = gc.open_by_key("你的GoogleSheetID").sheet1
    records = sheet.get_all_records()
    return {"data": records}

# --------------------------
# Render 啟動用
# --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
