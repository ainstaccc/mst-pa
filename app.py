import os
import json
from flask import Flask
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# --------------------------
# 1️⃣ Google Sheets 驗證
# --------------------------
# 從環境變數讀取 JSON 金鑰
service_account_info = json.loads(os.environ["GOOGLE_SHEETS_KEY"])
creds = Credentials.from_service_account_info(
    service_account_info,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ],
)
gc = gspread.authorize(creds)

# Google Sheet ID
SHEET_ID = "1ZNjTzRepFjwikGpTt8QpnyHmarW6iCKkJzaCyXHApWw"

@app.route("/")
def index():
    try:
        # 讀取第一個分頁
        sh = gc.open_by_key(SHEET_ID)
        ws = sh.sheet1
        data = ws.get_all_values()  # 取得整個表格資料
        
        # 只顯示前 5 筆，避免太長
        preview = "<br>".join([str(row) for row in data[:5]])
        return f"<h3>✅ 成功讀取 Google Sheet！</h3><pre>{preview}</pre>"
    except Exception as e:
        return f"<h3>❌ 讀取失敗</h3><pre>{str(e)}</pre>"

# --------------------------
# 2️⃣ Render 啟動
# --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
