import sqlite3
from app.config.settings import DATABASE_NAME


def get_connection():
    """Get database connection"""
    return sqlite3.connect(DATABASE_NAME)


def init_db():
    """Initialize database with all required tables"""
    conn = sqlite3.connect(DATABASE_NAME)
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

    conn.commit()
    conn.close()
    print("Database initialized successfully")