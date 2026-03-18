import sqlite3
from app.config.settings import DATABASE_NAME


def get_connection():
    """Get database connection"""
    return sqlite3.connect(DATABASE_NAME)


def init_db():
    """Initialize database with all required tables"""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Department table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Department (
        dept_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL
    )
    """)

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
        emp_pass TEXT,
        dept_ID INTEGER,
        FOREIGN KEY(dept_ID) REFERENCES Department(dept_ID)
    )
    """)

    # Admin table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Admin (
        admin_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
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
        in_time TEXT,
        out_time TEXT,
        status TEXT,
        early_leave_approved INTEGER DEFAULT 0,
        FOREIGN KEY(employee_ID) REFERENCES Employee(employee_ID),
        FOREIGN KEY(job_ID) REFERENCES Job_Title(job_ID)
    )
    """)

    # Ensure dept_ID exists on Employee for older databases
    c.execute("PRAGMA table_info(Employee)")
    columns = [row[1] for row in c.fetchall()]
    if "dept_ID" not in columns:
        c.execute("ALTER TABLE Employee ADD COLUMN dept_ID INTEGER")

    # Ensure On_Duty has time tracking columns for older databases
    c.execute("PRAGMA table_info(On_Duty)")
    duty_columns = {row[1] for row in c.fetchall()}
    if "in_time" not in duty_columns:
        c.execute("ALTER TABLE On_Duty ADD COLUMN in_time TEXT")
    if "out_time" not in duty_columns:
        c.execute("ALTER TABLE On_Duty ADD COLUMN out_time TEXT")
    if "status" not in duty_columns:
        c.execute("ALTER TABLE On_Duty ADD COLUMN status TEXT")
    if "early_leave_approved" not in duty_columns:
        c.execute("ALTER TABLE On_Duty ADD COLUMN early_leave_approved INTEGER DEFAULT 0")

    conn.commit()
    conn.close()
    print("Database initialized successfully")
