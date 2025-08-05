from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# 讀取你的 Excel 檔
EXCEL_PATH = "2025.07 門市-考核總表_查詢平台.xlsx"
df = pd.read_excel(EXCEL_PATH)

@app.route('/', methods=['GET', 'POST'])
def home():
    keyword = ""
    results_html = None

    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        if keyword:
            # 模糊搜尋所有欄位
            mask = df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
            results = df[mask]

            if not results.empty:
                results_html = results.to_html(classes='table table-bordered table-striped', index=False)

    return render_template("index.html", keyword=keyword, results_html=results_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
