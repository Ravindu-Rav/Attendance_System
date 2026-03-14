"""Employee Repository - Data access layer for Employee"""
from app.database.db import get_connection


class EmployeeRepository:
    @staticmethod
    def get_all_employees():
        """Get all employees"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT employee_ID, fname, lname FROM Employee")
        employees = c.fetchall()
        conn.close()
        return employees

    @staticmethod
    def create_employee(employee_id, fname, lname, gender=1, age=25, email=None, password="password123"):
        """Create new employee"""
        if email is None:
            email = f"{fname.lower()}@company.com"
        
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
        INSERT INTO Employee (employee_ID, fname, lname, gender, age, emp_email, emp_pass)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (employee_id, fname, lname, gender, age, email, password))
        conn.commit()
        conn.close()
        return employee_id

    @staticmethod
    def update_employee(employee_id, fname, lname):
        """Update employee name"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE Employee SET fname = ?, lname = ? WHERE employee_ID = ?",
                 (fname, lname, employee_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_employee(employee_id):
        """Delete employee"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM Employee WHERE employee_ID = ?", (employee_id,))
        conn.commit()
        conn.close()