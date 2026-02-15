print("hello world")

import sqlite3
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Connect to database (creates file if not exists)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# Create users with different passwords
users = [
    ("atulya", "b25256@iitmandi.ac.in",
     bcrypt.generate_password_hash("student123").decode("utf-8"), "student"),

     ("pratha", "faculty01@iitmandi.ac.in",
     bcrypt.generate_password_hash("faculty123").decode("utf-8"), "faculty"),

    ("Admin User", "admin01@iitmandi.ac.in",
     bcrypt.generate_password_hash("admin123").decode("utf-8"), "admin"),

    ("Authority User", "authority01@iitmandi.ac.in",
     bcrypt.generate_password_hash("authority123").decode("utf-8"), "authority")
]

# Insert users
for user in users:
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", user
        )
    except:
        pass  # ignore if already exists

conn.commit()
conn.close()

print("Database setup complete and users added.")
