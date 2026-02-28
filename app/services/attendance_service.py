from app.database.db import get_connection
from datetime import datetime

def mark_attendance(employee_id):

    conn = get_connection()
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    c.execute("""
        INSERT INTO On_Duty(employee_ID, duration, date)
        VALUES (?, ?, ?)
    """, (employee_id, 8, today))

    conn.commit()
    conn.close()