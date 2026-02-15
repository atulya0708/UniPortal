from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "secret123"
bcrypt = Bcrypt(app)

def get_db():
    return sqlite3.connect("database.db")

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

#login page
@app.route("/")
def start():
    return render_template("start.html")

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, password, role FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        name, stored_password, role = user

        if bcrypt.check_password_hash(stored_password, password):
            session["name"] = name
            session["role"] = role

            if role == "student":
                return redirect(url_for("dashboard"))
            elif role == "faculty":
                return redirect(url_for("faculty_dashboard"))
            elif role == "admin":
                return redirect(url_for("admin_dashboard"))
            elif role == "authority":
                return redirect(url_for("authority_dashboard"))

    return "Invalid Login"



@app.route("/dashboard")
def dashboard():
    if "role" not in session or session["role"] != "student":
        return redirect(url_for("login_page"))
    return render_template("dashboard.html")

@app.route("/faculty_dashboard")
def faculty_dashboard():
    if "role" not in session or session["role"] != "faculty":
        return redirect(url_for("login_page"))
    return render_template("faculty_dashboard.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login_page"))
    return render_template("admin_dashboard.html")
    
@app.route("/authority_dashboard")
def authority_dashboard():
    if "role" not in session or session["role"] != "authority":
        return redirect(url_for("login_page"))
    return render_template("authority_dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("start"))


if __name__ == "__main__":
    app.run(debug=True)

