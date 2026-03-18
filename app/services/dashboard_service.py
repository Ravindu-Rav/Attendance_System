from datetime import datetime, timedelta
from app.database.db import get_connection
from app.services.attendance_logic_service import (
    calculate_worked_hours,
    calculate_late_hours,
    calculate_extra_hours,
)


def get_dashboard_stats():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM Employee")
    total_employees = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Department")
    total_departments = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Job_Title")
    total_job_titles = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM Admin")
    total_admins = cur.fetchone()[0]

    today = datetime.now().strftime("%Y-%m-%d")
    cur.execute("SELECT COUNT(*), COALESCE(AVG(duration), 0) FROM On_Duty WHERE date = ?", (today,))
    row = cur.fetchone()
    today_attendance = row[0]
    avg_duration = row[1] or 0

    cur.execute("SELECT in_time, out_time FROM On_Duty WHERE date = ?", (today,))
    extra_hours_total = 0.0
    late_hours_total = 0.0
    for in_time, out_time in cur.fetchall():
        late_hours_total += calculate_late_hours(in_time)
        extra_hours_total += calculate_extra_hours(out_time)

    absent = max(total_employees - today_attendance, 0)
    rate = 0
    if total_employees:
        rate = int((today_attendance / total_employees) * 100)

    conn.close()
    return {
        "total_employees": total_employees,
        "total_departments": total_departments,
        "total_job_titles": total_job_titles,
        "total_admins": total_admins,
        "today_attendance": today_attendance,
        "avg_duration": avg_duration,
        "absent": absent,
        "rate": rate,
        "extra_hours_total": extra_hours_total,
        "late_hours_total": late_hours_total,
    }


def get_trend_counts():
    conn = get_connection()
    cur = conn.cursor()
    start_date = datetime.now().date() - timedelta(days=6)
    dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    counts = {d: 0 for d in dates}

    cur.execute(
        "SELECT date, COUNT(*) FROM On_Duty WHERE date BETWEEN ? AND ? GROUP BY date",
        (dates[0], dates[-1]),
    )
    for date_str, count in cur.fetchall():
        if date_str in counts:
            counts[date_str] = count

    conn.close()
    return dates, counts


def get_departments_overview():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT d.department_name, COUNT(e.employee_ID) AS emp_count
        FROM Department d
        LEFT JOIN Employee e ON e.dept_ID = d.dept_ID
        GROUP BY d.dept_ID
        ORDER BY emp_count DESC, d.department_name ASC
        LIMIT 6
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_admins():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT admin_ID, username, created_at
        FROM Admin
        ORDER BY created_at DESC, admin_ID DESC
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_early_leave_requests():
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cur.execute(
        """
        SELECT o.duty_ID,
               e.fname || ' ' || e.lname AS full_name,
               o.in_time,
               o.early_leave_approved
        FROM On_Duty o
        LEFT JOIN Employee e ON o.employee_ID = e.employee_ID
        WHERE o.date = ? AND o.out_time IS NULL
        ORDER BY o.in_time ASC
        """,
        (today,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def approve_early_leave(duty_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE On_Duty SET early_leave_approved = 1 WHERE duty_ID = ?", (duty_id,))
    conn.commit()
    conn.close()


def get_attendance_records(date_str=None):
    conn = get_connection()
    cur = conn.cursor()
    if date_str:
        cur.execute(
            """
            SELECT e.fname || ' ' || e.lname AS full_name,
                   COALESCE(j.job_title, 'N/A') AS job_title,
                   o.date,
                   o.in_time,
                   o.out_time,
                   COALESCE(o.duration, 0),
                   COALESCE(o.status, '')
            FROM On_Duty o
            LEFT JOIN Employee e ON o.employee_ID = e.employee_ID
            LEFT JOIN Job_Title j ON o.job_ID = j.job_ID
            WHERE o.date = ?
            ORDER BY o.date DESC, o.duty_ID DESC
            """,
            (date_str,),
        )
    else:
        cur.execute(
            """
            SELECT e.fname || ' ' || e.lname AS full_name,
                   COALESCE(j.job_title, 'N/A') AS job_title,
                   o.date,
                   o.in_time,
                   o.out_time,
                   COALESCE(o.duration, 0),
                   COALESCE(o.status, '')
            FROM On_Duty o
            LEFT JOIN Employee e ON o.employee_ID = e.employee_ID
            LEFT JOIN Job_Title j ON o.job_ID = j.job_ID
            ORDER BY o.date DESC, o.duty_ID DESC
            """
        )
    rows = cur.fetchall()
    conn.close()
    return rows
