import os
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# Excel 檔案路徑
EXCEL_FILE = os.path.join("data", "2025.07 門市-考核總表_查詢平台.xlsx")

# 目標分頁
TARGET_SHEETS = ["等級分佈", "門店 考核總表", "人效分析", "店主管 考核明細", "店員 考核明細"]

@app.route("/")
def index():
    results = {}
    try:
        # 逐一讀取各分頁
        for sheet in TARGET_SHEETS:
            df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)
            results[sheet] = df.head(10).to_html(classes="table table-striped", index=False)
        
        return render_template("index.html", results=results, sheets=TARGET_SHEETS)

    except Exception as e:
        return f"<h1>❌ 讀取失敗</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run(debug=True)
