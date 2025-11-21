import sqlite3

conn = sqlite3.connect('school_db.db')
c = conn.cursor()

# Table: class_schedule
c.execute('''CREATE TABLE IF NOT EXISTS class_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT,
    day TEXT,
    time TEXT
)''')

# Table: grades 
c.execute('''CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT,
    grade TEXT
)''')

# Table: homework
c.execute('''CREATE TABLE IF NOT EXISTS homework (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT,
    due_date TEXT,
    assignment_name TEXT,
    category TEXT,
    status TEXT DEFAULT 'not started'
)''')

conn.commit()
conn.close()
print("School database created successfully.")
