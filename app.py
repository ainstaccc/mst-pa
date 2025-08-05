import os
import json
from flask import Flask
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# --------------------------
# 1️⃣ Google Sheets 驗證
# --------------------------
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

# 要讀取的分頁名稱
TARGET_SHEETS = [
    "等級分佈",
    "門店 考核總表",
    "人效分析",
    "店主管 考核明細",
    "店員 考核明細",
]

@app.route("/")
def index():
    try:
        sh = gc.open_by_key(SHEET_ID)
        output_html = "<h2>✅ 成功讀取 Google Sheet</h2>"
        
        for sheet_name in TARGET_SHEETS:
            try:
                ws = sh.worksheet(sheet_name)
                data = ws.get_all_values()
                preview = "<br>".join([str(row) for row in data[:5]])  # 只取前5列
                output_html += f"<h3>📄 {sheet_name}</h3><pre>{preview}</pre><hr>"
            except Exception as e:
                output_html += f"<h3>📄 {sheet_name} ❌ 讀取失敗</h3><pre>{str(e)}</pre><hr>"

        return output_html

    except Exception as e:
        return f"<h3>❌ 整體讀取失敗</h3><pre>{str(e)}</pre>"

# --------------------------
# 2️⃣ Render 啟動
# --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
