from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # セッション管理用の秘密鍵（変更推奨）

# CSVファイルのパス
CSV_FILE = "data.csv"

# 管理者のログイン情報（カスタマイズ可）
ADMIN_USERNAME = "yoshitake.customer@gmail.com"
ADMIN_PASSWORD = "password123roger"

# 銘柄リストの表示ページ
@app.route('/')
def index():
    if not os.path.exists(CSV_FILE):
        return "データファイルが存在しません"
    
    df = pd.read_csv(CSV_FILE)
    return render_template("index.html", data=df.to_dict(orient="records"))

# 管理ページ（ログインしないとアクセス不可）
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if "logged_in" not in session:  # 未ログインならログインページへリダイレクト
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(CSV_FILE)
            return redirect(url_for('index'))
    return render_template("admin.html")

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True  # セッションにログイン情報を保存
            return redirect(url_for('admin'))
        else:
            return "ログイン失敗。やり直してください。"
    return render_template("login.html")

# ログアウト処理
@app.route('/logout')
def logout():
    session.pop("logged_in", None)  # セッション情報を削除
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
