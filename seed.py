import sqlite3

def seed_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Clear existing assignments to avoid duplicates
    cursor.execute("DELETE FROM assignments")

    # Add assignments for different batches to test the filter logic
    test_data = [
        # Subject, Task, Deadline, Target Batch
        ('Data Structures', 'Lab 5: Trees', '2026-02-20', 'B25'),
        ('Calculus', 'Integrals Quiz', '2026-02-22', 'B25'),
        ('Physics', 'Quantum Mechanics HW', '2026-03-01', 'B24'),
        ('Chemistry', 'Organic Synthesis Report', '2026-02-28', 'B23'),
        ('General', 'Hostel Feedback Form', '2026-03-15', 'ALL') # Visible to everyone
    ]

    cursor.executemany(
        "INSERT INTO assignments (subject, task_name, deadline, target_batch) VALUES (?, ?, ?, ?)",
        test_data
    )

    conn.commit()
    conn.close()
    print("Database seeded with assignments for multiple batches (B23, B24, B25)!")

if __name__ == "__main__":
    seed_database()