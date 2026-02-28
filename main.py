import sqlite3

def init_db():
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()

    # Employee table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Employee (
        employee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        fname TEXT NOT NULL,
        lname TEXT NOT NULL,
        gender INTEGER,
        age INTEGER,
        contact_add TEXT,
        emp_email TEXT UNIQUE,
        emp_pass TEXT
    )
    """)

    # Department table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Department (
        dept_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL
    )
    """)

    # Job Title table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Job_Title (
        job_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT NOT NULL,
        dept_ID INTEGER,
        employee_ID INTEGER,
        FOREIGN KEY(dept_ID) REFERENCES Department(dept_ID),
        FOREIGN KEY(employee_ID) REFERENCES Employee(employee_ID)
    )
    """)

    # On Duty table (attendance from face scan)
    c.execute("""
    CREATE TABLE IF NOT EXISTS On_Duty (
        duty_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_ID INTEGER,
        job_ID INTEGER,
        duration INTEGER,
        date TEXT,
        FOREIGN KEY(employee_ID) REFERENCES Employee(employee_ID),
        FOREIGN KEY(job_ID) REFERENCES Job_Title(job_ID)
    )
    """)

    # Leave table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Leave_Record (
        leave_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_ID INTEGER,
        job_ID INTEGER,
        date TEXT,
        FOREIGN KEY(emp_ID) REFERENCES Employee(employee_ID),
        FOREIGN KEY(job_ID) REFERENCES Job_Title(job_ID)
    )
    """)

    # Attendance Reports
    c.execute("""
    CREATE TABLE IF NOT EXISTS Attendance_Report (
        report_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_ID INTEGER,
        job_ID INTEGER,
        duty_ID INTEGER,
        total_labor INTEGER,
        salary INTEGER,
        date TEXT,
        FOREIGN KEY(employee_ID) REFERENCES Employee(employee_ID),
        FOREIGN KEY(job_ID) REFERENCES Job_Title(job_ID),
        FOREIGN KEY(duty_ID) REFERENCES On_Duty(duty_ID)
    )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()