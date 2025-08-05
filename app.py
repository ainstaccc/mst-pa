import os
from flask import Flask, render_template_string
import gspread
from google.oauth2.service_account import Credentials

# --------------------------
# 1️⃣ 建立 Flask App
# --------------------------
app = Flask(__name__)

# --------------------------
# 2️⃣ Google Sheets 驗證
# --------------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_FILE = "service_account.json"  # 金鑰檔案放在專案根目錄

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

# 替換成你的 Google Sheet ID
SHEET_ID = "1ZNjTzRepFjwikGpTt8QpnyHmarW6iCKkJzaCyXHApWw"
WORKSHEET_NAME = "人效分析"  # 先測試單一分頁

# --------------------------
# 3️⃣ 首頁：測試讀取 Google Sheet
# --------------------------
@app.route('/')
def index():
    try:
        sh = gc.open_by_key(SHEET_ID)
        ws = sh.worksheet(WORKSHEET_NAME)
        data = ws.get_all_values()  # 讀取整個表格

        # 簡單顯示成 HTML 表格
        table_html = "<table border='1'>" + "".join(
            f"<tr>{''.join(f'<td>{cell}</td>' for cell in row)}</tr>" for row in data
        ) + "</table>"
        return render_template_string("<h2>Google Sheet 資料測試</h2>" + table_html)
    except Exception as e:
        return f"<h3>讀取 Google Sheet 失敗</h3><pre>{str(e)}</pre>"

# --------------------------
# 4️⃣ Render 啟動
# --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
