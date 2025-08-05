import os
import json
from flask import Flask, request, render_template_string
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --------------------------
# Flask App 初始化
# --------------------------
app = Flask(__name__)

# --------------------------
# Google Sheets 授權
# --------------------------
# 讀取 Render 環境變數
SPREADSHEET_ID = os.environ.get("GOOGLE_SHEET_ID")  # 例如: 1ZNjTzRepFjwikGpTt8QpnyHmarW6iCKkJzaCyXHApWw
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")  # JSON字串

# 權限範圍
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

# 解析 JSON 並授權
creds_dict = json.loads(GOOGLE_CREDENTIALS)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# --------------------------
# 首頁：簡單查詢表單
# --------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    query_result = []
    if request.method == "POST":
        manager_name = request.form.get("manager_name")
        worksheet = client.open_by_key(SPREADSHEET_ID).worksheet("門店 考核總表")
        data = worksheet.get_all_values()

        # 取得表頭與資料列
        header = data[0]
        rows = data[1:]

        # 篩選區主管名稱 (假設在 B 欄)
        for row in rows:
            if len(row) > 1 and manager_name in row[1]:
                query_result.append(row)

        return render_template_string(HTML_TEMPLATE, result=query_result, header=header)

    return render_template_string(HTML_TEMPLATE, result=None, header=None)

# --------------------------
# HTML 模板
# --------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>門市考核查詢平台</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 5px; text-align: center; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2>門市考核查詢平台</h2>
    <form method="POST">
        區主管姓名: <input type="text" name="manager_name" required>
        <button type="submit">查詢</button>
    </form>

    {% if result %}
        <h3>查詢結果 (共 {{ result|length }} 筆)</h3>
        <table>
            <tr>
                {% for col in header %}
                    <th>{{ col }}</th>
                {% endfor %}
            </tr>
            {% for row in result %}
                <tr>
                    {% for col in row %}
                        <td>{{ col }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </table>
    {% elif result is not none %}
        <p>查無資料</p>
    {% endif %}
</body>
</html>
"""

# --------------------------
# Render 用入口
# --------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
