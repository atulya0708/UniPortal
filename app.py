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
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

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
    if session.get("role") != "admin":
        return redirect(url_for("login_page"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total_complaints = cursor.fetchone()[0]

    cursor.execute("SELECT name, email, role FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT action, timestamp FROM logs ORDER BY id DESC LIMIT 10")
    logs = cursor.fetchall()

    cursor.execute("SELECT name, email, role FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_complaints=total_complaints,
        users=users,
        logs=logs
    )
    
@app.route("/authority_dashboard")
def authority_dashboard():
    if "role" not in session or session["role"] != "authority":
        return redirect(url_for("login_page"))
    return render_template("authority_dashboard.html")

@app.route("/clubs")
def clubs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clubs")
    clubs = cursor.fetchall()
    conn.close()

    return render_template("clubs.html", clubs=clubs)

@app.route("/join_club/<int:club_id>", methods=["POST"])
def join_club(club_id):
    email = session["email"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO club_members (club_id, email) VALUES (?, ?)",
        (club_id, email)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("clubs"))

@app.route("/add_announcement", methods=["GET", "POST"])
def add_announcement():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO announcements (title, content, category) VALUES (?, ?, ?)",
            (title, content, category)
        )

        conn.commit()
        conn.close()

    return render_template("add_announcement.html")

@app.route("/announcements")
def announcements():
    conn = get_db()
    cursor = conn.cursor()

    category = request.args.get("category")

    if category:
        cursor.execute(
            "SELECT * FROM announcements WHERE category=? ORDER BY created_at DESC",
            (category,)
        )
    else:
        cursor.execute(
            "SELECT * FROM announcements ORDER BY created_at DESC"
        )

    announcements = cursor.fetchall()
    conn.close()

    return render_template("announcements.html", announcements=announcements)

    


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("start"))

@app.route("/test")
def test():
    return "Server working"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)

