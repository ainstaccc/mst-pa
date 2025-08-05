from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# 讀取 Google Sheet 共享連結 (將網址轉換為 CSV 下載連結)
# 你的 XLS 純文字檔案 Google Sheet
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/192JCsp3kl4Hr-87546f_d4VbZt9kEdJP/export?format=csv"

# 載入資料
def load_data():
    try:
        df = pd.read_csv(GOOGLE_SHEET_URL)
        return df
    except Exception as e:
        print("讀取 Google Sheet 失敗：", e)
        return pd.DataFrame()

@app.route("/", methods=["GET", "POST"])
def index():
    df = load_data()
    if df.empty:
        return "<h2>讀取 Google Sheet 失敗，請檢查連結或權限</h2>"

    keyword = ""
    results_html = None

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()
        if keyword:
            results = df[df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
            results_html = results.to_html(classes='table table-striped', index=False)

    return render_template("index.html", keyword=keyword, results_html=results_html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
