# UniPortal – Smart Campus Management System

UniPortal is a web-based campus management platform built using **Flask** that integrates academic tracking, opportunities, clubs, announcements, and dashboards into a unified portal for students, faculty, and administrators.

The system is designed to reduce fragmentation between university services by providing a single, role-based interface.

---

## Features

### Authentication & Roles

* Secure login system
* Role-based dashboards:

  * Student
  * Faculty
  * Admin
  * Authority
* Password hashing using **Flask-Bcrypt**
* Session management

---

### Pillar II – Clubs & Announcements

* View and join campus clubs
* Club member management
* University announcements
* Category filtering for notices

---

### Pillar III – Academic Management

* Assignment tracking
* Exam schedules
* Attendance and credits (Samarth integration template)
* LMS assignment fetching (Moodle API template)
* Resource repository (Vault of Knowledge)
* Grievance tracking system
* Academic dashboard with statistics

---

### Pillar IV – Opportunities & Personal Tasks

* Faculty research / internship postings
* Student applications
* Personal task manager (Scholar’s Ledger)
* Deadline tracking

---

### Dashboard Features

* Chronos Calendar for assignments and exams
* Academic statistics display
* Dark / Light mode toggle
* Tab-based navigation

---

## Tech Stack

**Backend**

* Python
* Flask
* SQLite

**Frontend**

* HTML
* CSS
* JavaScript
* Jinja2 Templates
* FontAwesome Icons

**Libraries Used**

* flask-bcrypt
* requests
* beautifulsoup4

---

## Project Structure

```
UniPortal/
│
├── app.py
├── database.db
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── admin_dashboard.html
│   ├── faculty_dashboard.html
│   ├── announcements.html
│   ├── clubs.html
│   ├── opportunities.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── README.md
```

---

## Installation & Setup

### 1. Clone the Repository

```
git clone <repository-url>
cd UniPortal
```

---

### 2. Create Virtual Environment

Mac/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

Windows:

```
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```
pip install flask
pip install flask-bcrypt
pip install requests
pip install beautifulsoup4
```

---

### 4. Run the Application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5002
```

---

## Database

SQLite database initializes automatically using:

```
init_db()
```

Tables include:

* users
* assignments
* grievances
* resources
* opportunities
* applications
* personal_tasks
* announcements
* clubs
* logs

---

## Future Improvements

* Real LMS API integration
* File upload system for resources
* Notification system
* Email alerts
* Deployment on cloud
* Mobile-friendly UI

---

## Authors

Developed as part of a university system project.

---

## License

This project is for educational and academic purposes.
