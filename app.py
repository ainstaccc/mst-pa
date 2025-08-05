from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# 直接用 CSV 連結
CSV_URL = "https://docs.google.com/spreadsheets/d/192JCsp3kl4Hr-87546f_d4VbZt9kEdJP/export?format=csv&gid=1006342564"

@app.route('/', methods=["GET", "POST"])
def home():
    keyword = ""
    results_html = ""

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()

        # 讀取 Google Sheet (CSV)
        df = pd.read_csv(CSV_URL)

        # 關鍵字搜尋
        if keyword:
            mask = df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
            results = df[mask]

            if not results.empty:
                results_html = results.to_html(classes="table table-striped", index=False)

    return render_template("index.html", keyword=keyword, results_html=results_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
