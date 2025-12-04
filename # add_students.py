import sqlite3

conn = sqlite3.connect('school.db')
c = conn.cursor()

students = [
    ("student1", "12345", "Student one"),("student2", "54321", "Student Two")
]

for s in students:
    c.execute("INSERT OR IGNORE INTO students (username, password, full_name) VALUES (?, ?, ?)", s)

conn.commit()
conn.close()
print("Sample students added.")

