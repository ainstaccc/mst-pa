import os, json
from flask import Flask
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

@app.route("/")
def index():
    try:
        creds = Credentials.from_service_account_info(
            json.loads(os.environ["GOOGLE_CREDENTIALS"]),
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets.readonly",
                "https://www.googleapis.com/auth/drive.readonly",
            ],
        )
        gc = gspread.authorize(creds)

        sh = gc.open_by_key("1ZNjTzRepFjwikGpTt8QpnyHmarW6iCKkJzaCyXHApWw")
        ws = sh.worksheet("等級分佈")
        data = ws.get_all_values()
        preview = "<br>".join([str(row) for row in data[:5]])

        return f"<h2>✅ 成功讀取 Google Sheet</h2><pre>{preview}</pre>"

    except Exception as e:
        return f"<h3>❌ 讀取失敗</h3><pre>{str(e)}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
