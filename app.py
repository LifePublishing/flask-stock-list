from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # セッション管理用の秘密鍵（変更推奨）

# CSVファイルのパス
CSV_FILE = "data.csv"

# **閲覧ページ用の認証情報**
CUSTOMER_PASSWORD = "test123"
CUSTOMER_USERS = ["user1", "user2", "user3"]  # ここにお客様のユーザーIDを追加

# **管理ページ用の認証情報**
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# **閲覧ページ（ログインが必要）**
@app.route('/', methods=['GET', 'POST'])
def index():
    # 🔹 お客様のログインセッションがない場合は、ログインページへリダイレクト
    if "customer_logged_in" not in session:
        return redirect(url_for('customer_login'))

    if not os.path.exists(CSV_FILE):
        return "データファイルが存在しません"

    df = pd.read_csv(CSV_FILE)
    return render_template("index.html", data=df.to_dict(orient="records"))

# **お客様用ログインページ**
@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in CUSTOMER_USERS and password == CUSTOMER_PASSWORD:
            session["customer_logged_in"] = True  # ✅ ログインセッションを設定
            return redirect(url_for('index'))
        else:
            return "ログイン失敗。やり直してください。"

    return render_template("customer_login.html")

# **管理ページ（ログインが必要）**
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if "admin_logged_in" not in session:
        return redirect(url_for('login'))  # 未ログインならログインページへ
    
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(CSV_FILE)
            return redirect(url_for('index'))
    return render_template("admin.html")

# **管理者ログイン**
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for('admin'))
        else:
            return "ログイン失敗。やり直してください。"
    return render_template("login.html")

# **ログアウト（管理者・お客様共通）**
@app.route('/logout')
def logout():
    session.pop("admin_logged_in", None)
    session.pop("customer_logged_in", None)
    return redirect(url_for('customer_login'))  # ✅ ログアウト後はログインページへ

if __name__ == '__main__':
    app.run(debug=True)
