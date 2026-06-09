from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

# Database Creation
def init_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll_no TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']

        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students(name, roll_no) VALUES (?, ?)",
            (name, roll_no)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_student.html')

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if request.method == 'POST':

        for student in students:
            status = request.form.get(str(student[0]))

            cursor.execute(
                "INSERT INTO attendance(student_id,date,status) VALUES (?,?,?)",
                (student[0], date.today(), status)
            )

        conn.commit()
        conn.close()

        return redirect('/view_attendance')

    conn.close()
    return render_template(
        'mark_attendance.html',
        students=students
    )

@app.route('/view_attendance')
def view_attendance():

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT students.name,
           students.roll_no,
           attendance.date,
           attendance.status
    FROM attendance
    JOIN students
    ON students.id = attendance.student_id
    ''')

    records = cursor.fetchall()

    conn.close()

    return render_template(
        'view_attendance.html',
        records=records
    )

if __name__ == '__main__':
    app.run(debug=True)