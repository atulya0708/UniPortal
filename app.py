from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "iit_mandi_portal_key"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row 
    return conn

# --- DATABASE INITIALIZATION ---
def init_db():
    conn = get_db()
    # PILLAR III TABLES
    conn.execute('''CREATE TABLE IF NOT EXISTS assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, 
                    task_name TEXT, deadline DATE, target_batch TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS grievances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, 
                    title TEXT, category TEXT, priority TEXT, 
                    description TEXT, status TEXT DEFAULT 'Submitted', 
                    date_posted DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    course_code TEXT, course_name TEXT, 
                    resource_type TEXT, file_url TEXT, 
                    professor TEXT, semester TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS student_courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    roll_no TEXT, course_code TEXT, 
                    credits REAL, attendance_count INTEGER DEFAULT 0, 
                    total_classes INTEGER DEFAULT 0)''')

    # PILLAR IV TABLES (NEW)
    # Faculty Research/Internship Postings
    conn.execute('''CREATE TABLE IF NOT EXISTS opportunities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    faculty_id TEXT, title TEXT, description TEXT,
                    required_skills TEXT, duration TEXT, stipend TEXT,
                    deadline DATE, department TEXT, status TEXT DEFAULT 'Open')''')

    # Student Applications to those opportunities
    conn.execute('''CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    opp_id INTEGER, student_roll TEXT, resume_url TEXT,
                    status TEXT DEFAULT 'Submitted', applied_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(opp_id) REFERENCES opportunities(id))''')

    # The Scholar's Ledger (Personal Task Manager)
    conn.execute('''CREATE TABLE IF NOT EXISTS personal_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_roll TEXT, task_title TEXT, category TEXT,
                    deadline DATE, status TEXT DEFAULT 'Pending')''')
    
    conn.commit()
    conn.close()

# Run the unified initialization
init_db()

# --- REAL-TIME FETCHING HELPERS (Pillar III) ---

def fetch_lms_data():
    """Fetches real assignments using Moodle Web Service API."""
    # Note: Replace with your actual token from LMS preferences
    MOODLE_TOKEN = "YOUR_MOODLE_TOKEN_HERE" 
    LMS_URL = "https://lms.iitmandi.ac.in/webservice/rest/server.php"
    
    params = {
        'wstoken': MOODLE_TOKEN,
        'wsfunction': 'mod_assign_get_assignments',
        'moodlewsrestformat': 'json'
    }
    
    try:
        response = requests.get(LMS_URL, params=params, timeout=5)
        data = response.json()
        assignments = []
        for course in data.get('courses', []):
            for assign in course.get('assignments', []):
                due_date = datetime.fromtimestamp(assign['duedate']).strftime('%Y-%m-%d')
                assignments.append({
                    'subject': course['shortname'],
                    'task_name': f"LMS: {assign['name']}",
                    'deadline': due_date,
                    'source': 'LMS'
                })
        return assignments
    except:
        return []

def fetch_samarth_stats(roll_no, password="DEFAULT_PASSWORD"):
    """Scrapes attendance and credits from Samarth Portal."""
    # This is a template; real scraping requires valid student credentials
    try:
        # Simulated successful scrape result based on Pillar III requirements
        return {
            'attendance': 85.5, 
            'credits': 18.0,
            'courses': 6
        }
    except:
        return {'attendance': 0.0, 'credits': 0.0, 'courses': 0}

# --- ROUTES ---

@app.route("/")
def home():
    return redirect(url_for("login_page"))

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
<<<<<<< HEAD
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


=======
    email = request.form["email"].lower()
    if email.endswith("@students.iitmandi.ac.in"):
        session["email"] = email 
        session["role"] = "student"
        return redirect(url_for("dashboard"))
    return "Invalid Login: Use your @students.iitmandi.ac.in email."
>>>>>>> b101d6c (whole project)



@app.route("/dashboard")
def dashboard():
    if "role" not in session:
        return redirect(url_for("login_page"))
<<<<<<< HEAD
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
=======
>>>>>>> b101d6c (whole project)
    
    email = session.get("email")
    roll_no = email.split('@')[0].upper()
    batch_prefix = roll_no[:3]

    # 1. Fetch Real-time Data from Samarth & LMS
    samarth_data = fetch_samarth_stats(roll_no)
    lms_assignments = fetch_lms_data()

    # 2. Fetch Local DB Data
    conn = get_db()
    
    # NEW: Academic Calendar - Specifically fetch Exam Schedules
    exam_schedules = conn.execute("""
        SELECT * FROM assignments 
        WHERE (target_batch = ? OR target_batch = 'ALL') 
        AND task_name LIKE '%Exam%' 
        ORDER BY deadline ASC""", (batch_prefix,)).fetchall()

    # Resource Repository - Fetch all available materials
    vault_resources = conn.execute("SELECT * FROM resources").fetchall()
    
    # Support Center - Fetch student grievances
    issues = conn.execute("SELECT * FROM grievances WHERE student_name = ? ORDER BY date_posted DESC", (roll_no,)).fetchall()
    
    # General Assignments logic
    db_tasks = conn.execute("SELECT * FROM assignments WHERE target_batch = ? OR target_batch = 'ALL'", (batch_prefix,)).fetchall()

    all_assignments = []
    today = date.today()

    for task in db_tasks:
        t_dict = dict(task)
        t_dict['source'] = 'Official'
        all_assignments.append(t_dict)

    # 3. Combine with LMS Data
    all_assignments.extend(lms_assignments)

    # 4. Calculate Deadlines for all tasks
    for task in all_assignments:
        try:
            d_date = datetime.strptime(task['deadline'], '%Y-%m-%d').date()
            task['days_remaining'] = (d_date - today).days
        except:
            task['days_remaining'] = "N/A"

    conn.close()
    
    # 5. Prepare stats object for "Destiny Manager"
    display_stats = {
        'total_credits': samarth_data['credits'],
        'total_courses': samarth_data['courses'],
        'avg_attendance': samarth_data['attendance']
    }

    # 6. Return all data to dashboard.html
    return render_template("dashboard.html", 
                           assignments=all_assignments, 
                           exams=exam_schedules, # For Chronos Calendar
                           issues=issues, 
                           roll_no=roll_no,
                           stats=display_stats, # For Course Management
                           vault=vault_resources) # For Resource Repository

# Browse Opportunities with smart filtering
@app.route("/opportunities")
def list_opportunities():
    dept = request.args.get('dept', '')
    conn = get_db()
    if dept:
        opps = conn.execute("SELECT * FROM opportunities WHERE department = ? AND status = 'Open'", (dept,)).fetchall()
    else:
        opps = conn.execute("SELECT * FROM opportunities WHERE status = 'Open'").fetchall()
    
    # Fetch student's own application history
    my_apps = conn.execute("SELECT a.*, o.title FROM applications a JOIN opportunities o ON a.opp_id = o.id WHERE a.student_roll = ?", 
                           (session.get('roll_no'),)).fetchall()
    conn.close()
    return render_template("opportunities.html", opps=opps, my_apps=my_apps)

# The Scholar's Ledger: Add Personal Task
@app.route("/add_personal_task", methods=["POST"])
def add_task():
    roll = session.get('roll_no')
    conn = get_db()
    conn.execute("INSERT INTO personal_tasks (student_roll, task_title, category, deadline) VALUES (?, ?, ?, ?)",
                 (roll, request.form['title'], request.form['category'], request.form['deadline']))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route("/search_resources")
def search_resources():
    query = request.args.get('query', '').strip()
    conn = get_db()
    if query:
        # Search by course code, professor, or topic
        search_sql = """SELECT * FROM resources 
                        WHERE course_code LIKE ? OR professor LIKE ? OR course_name LIKE ?"""
        filter_val = f"%{query}%"
        vault = conn.execute(search_sql, (filter_val, filter_val, filter_val)).fetchall()
    else:
        vault = conn.execute("SELECT * FROM resources").fetchall()
    conn.close()
    return render_template("dashboard.html", vault=vault, active_tab='vault')

@app.route("/upload_resource", methods=["POST"])
def upload_resource():
    # Implementation for student-uploadable materials
    # Logic to save file and insert metadata (course_code, prof, tags) into DB
    return redirect(url_for('dashboard'))

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
<<<<<<< HEAD
    return redirect(url_for("start"))

@app.route("/test")
def test():
    return "Server working"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)

=======
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> b101d6c (whole project)
