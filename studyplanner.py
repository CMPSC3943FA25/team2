"""This will import the libraries we need"""

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date
import sqlite3


app = Flask(__name__)

#Function for checking login, will check if username and password match with what is inside of our tables
def check_login(username, password):
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_name=? AND student_password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

#Function for our homepage
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if check_login(username, password):
        return redirect(url_for('calendar'))
    else:
        return "Invalid login."

#this function takes data from our database table "homework" and then sends it to our calender
@app.route('/calendar')
def calendar():
    selected_category = request.args.get('category', 'all')

    conn = sqlite3.connect('school.db')
    c = conn.cursor()

    if selected_category != 'all':
        c.execute(
            "SELECT id, class_name, assignment_name, due_date, category, status FROM homework WHERE category = ? ORDER BY due_date",
            (selected_category,)
        )
    else:
        c.execute(
            "SELECT id, class_name, assignment_name, due_date, category, status FROM homework ORDER BY due_date"
        )

    rows = c.fetchall()
    conn.close()

    
    homework_list = []
    today = date.today()

    for hw in rows:
        hw_id, class_name, assignment_name, due_date_str, category, status = hw

        days_left = None
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            delta = due_date - today
            days_left = delta.days
        except Exception:
            days_left = None 

        homework_list.append({
            "id": hw_id,
            "class_name": class_name,
            "assignment_name": assignment_name,
            "due_date": due_date_str,
            "category": category,
            "status": status,
            "days_left": days_left
        })
        
    conn2 = sqlite3.connect('school.db')
    c2 = conn2.cursor()
    c2.execute("SELECT class_id, difficulty FROM enrollment WHERE student_id = 1")
    diff_rows = c2.fetchall()
    conn2.close()

    difficulty_map = {r[0]: r[1] for r in diff_rows}

    for hw in homework_list:
        hw["difficulty"] = difficulty_map.get(hw["class_name"], 1)

    categories = ["all", "Homework", "Exam", "Quiz", "Project", "Other"]

    return render_template('calendar.html',
                           homework=homework_list,
                           categories=categories,
                           selected_category=selected_category)
    

@app.route('/update_status', methods=['POST'])
def update_status():
    hw_id = request.form['homework_id']
    new_status = request.form['status']

    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("UPDATE homework SET status = ? WHERE id = ?", (new_status, hw_id))
    conn.commit()
    conn.close()

    category = request.form.get('current_category', 'all')
    return redirect(url_for('calendar', category=category))

@app.route('/add_homework', methods=['GET', 'POST'])
def add_homework():
    if request.method == 'POST':
        class_name = request.form['class_name']
        assignment_name = request.form['assignment_name']
        due_date = request.form['due_date']
        category = request.form['category']

        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO homework (class_name, due_date, assignment_name, category, status) VALUES (?, ?, ?, ?, ?)",
            (class_name, due_date, assignment_name, category, 'not started')
        )
        conn.commit()
        conn.close()

        return redirect(url_for('calendar'))

    return render_template('add_homework.html')

@app.route('/delete_homework', methods=['POST'])
def delete_homework():
    hw_id = request.form['homework_id']

    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("DELETE FROM homework WHERE id = ?", (hw_id,))
    conn.commit()
    conn.close()

    category = request.form.get('current_category', 'all')
    return redirect(url_for('calendar', category=category))

@app.route('/set_difficulty', methods=['GET', 'POST'])
def set_difficulty():
    student_id = 1

    if request.method == 'POST':
        class_name = request.form['class_name']
        difficulty_level = int(request.form['difficulty_level'])

        conn = sqlite3.connect('school.db')
        c = conn.cursor()

        c.execute("""
            UPDATE class_difficulty
            SET difficulty_level = ?
            WHERE student_id = ? AND class_name = ?
        """, (difficulty_level, student_id, class_name))

        if c.rowcount == 0:
            c.execute("""
                INSERT INTO class_difficulty (student_id, class_name, difficulty_level)
                VALUES (?, ?, ?)
            """, (student_id, class_name, difficulty_level))

        conn.commit()
        conn.close()

        return redirect(url_for('set_difficulty'))

    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("""
        SELECT class_name, difficulty_level
        FROM class_difficulty
        WHERE student_id = ?
    """, (student_id,))
    rows = c.fetchall()
    conn.close()

    difficulties = [{"class_name": r[0], "difficulty_level": r[1]} for r in rows]

    return render_template('set_difficulty.html', difficulties=difficulties)


if __name__ == '__main__':
    app.run(debug=True)
