from app.database.db import get_connection
from datetime import datetime

def mark_attendance(employee_id):

    conn = get_connection()
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")

    c.execute("""
        INSERT INTO On_Duty(employee_ID, duration, date, in_time, status, early_leave_approved)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (employee_id, 0, today, now_time, "IN", 0))

    conn.commit()
    conn.close()
