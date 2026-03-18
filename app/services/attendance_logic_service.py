from datetime import datetime, time
from app.database.db import get_connection

WORK_START = time(8, 0, 0)
WORK_END = time(16, 0, 0)
REQUIRED_HOURS = 8.0


def _parse_time(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%H:%M:%S").time()
    except Exception:
        return None


def calculate_worked_hours(in_time_str, out_time_str):
    start = _parse_time(in_time_str)
    end = _parse_time(out_time_str)
    if not start or not end:
        return 0.0
    start_dt = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)
    return max((end_dt - start_dt).total_seconds() / 3600.0, 0.0)


def calculate_late_hours(in_time_str):
    start = _parse_time(in_time_str)
    if not start:
        return 0.0
    work_start_dt = datetime.combine(datetime.today(), WORK_START)
    in_dt = datetime.combine(datetime.today(), start)
    if in_dt <= work_start_dt:
        return 0.0
    return (in_dt - work_start_dt).total_seconds() / 3600.0


def calculate_extra_hours(out_time_str):
    end = _parse_time(out_time_str)
    if not end:
        return 0.0
    work_end_dt = datetime.combine(datetime.today(), WORK_END)
    out_dt = datetime.combine(datetime.today(), end)
    if out_dt <= work_end_dt:
        return 0.0
    return (out_dt - work_end_dt).total_seconds() / 3600.0


def _can_checkout(worked_hours, out_time_str, approved):
    if approved:
        return True
    if worked_hours < REQUIRED_HOURS:
        return False
    out_time = _parse_time(out_time_str)
    if not out_time:
        return False
    return out_time >= WORK_END


def mark_attendance(employee_id, mode):
    conn = get_connection()
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")

    c.execute(
        """
        SELECT duty_ID, in_time, out_time, early_leave_approved
        FROM On_Duty
        WHERE employee_ID = ? AND date = ?
        """,
        (employee_id, today),
    )
    row = c.fetchone()

    if mode == "in":
        if row:
            duty_id, in_time, out_time, _approved = row
            if in_time and not out_time:
                conn.close()
                return "Already Checked In"
            if out_time:
                conn.close()
                return "Already Checked Out"
            c.execute(
                """
                UPDATE On_Duty
                SET in_time = ?, status = 'IN'
                WHERE duty_ID = ?
                """,
                (now_time, duty_id),
            )
            conn.commit()
            conn.close()
            return "Checked In"

        c.execute(
            """
            INSERT INTO On_Duty(employee_ID, duration, date, in_time, status, early_leave_approved)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            (employee_id, 0, today, now_time, "IN", 0),
        )
        conn.commit()
        conn.close()
        return "Checked In"

    if mode == "out":
        if not row:
            conn.close()
            return "Not Checked In"

        duty_id, in_time, out_time, approved = row
        if not in_time:
            conn.close()
            return "Not Checked In"
        if out_time:
            conn.close()
            return "Already Checked Out"

        worked_hours = calculate_worked_hours(in_time, now_time)
        if not _can_checkout(worked_hours, now_time, approved):
            conn.close()
            return "No Approval"

        c.execute(
            """
            UPDATE On_Duty
            SET out_time = ?, duration = ?, status = 'OUT'
            WHERE duty_ID = ?
            """,
            (now_time, worked_hours, duty_id),
        )
        conn.commit()
        conn.close()
        return "Checked Out"

    conn.close()
    return "Error"


def get_today_attendance_list():
    conn = get_connection()
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute(
        """
        SELECT e.fname, e.lname, o.in_time, o.out_time, COALESCE(o.status, '')
        FROM On_Duty o
        JOIN Employee e ON o.employee_ID = e.employee_ID
        WHERE o.date = ?
        ORDER BY o.in_time DESC
        """,
        (today,),
    )
    rows = c.fetchall()
    conn.close()
    return rows
