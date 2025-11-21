import sqlite3

conn = sqlite3.connect('student_db.db')
c = conn.cursor()

# Students table
c.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    full_name TEXT
)''')

# Personal_schedules table
c.execute('''CREATE TABLE IF NOT EXISTS personal_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    day TEXT,
    study_time TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)''')

# Class_difficulty table
c.execute('''CREATE TABLE IF NOT EXISTS class_difficulty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    class_name TEXT,
    difficulty_level INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(id)
)''')

conn.commit()
conn.close()
print("Student database created successfully.")
