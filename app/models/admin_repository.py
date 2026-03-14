"""Admin Repository - Data access layer for Admin"""
from app.database.db import get_connection
from app.utils.password_utils import hash_password


class AdminRepository:
    @staticmethod
    def get_admin_by_credentials(username, password):
        """Get admin by username and password"""
        hashed_password = hash_password(password)
        
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM Admin WHERE username = ? AND password = ?", (username, hashed_password))
        admin = c.fetchone()
        conn.close()
        return admin

    @staticmethod
    def admin_exists():
        """Check if any admin exists"""
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM Admin")
        count = c.fetchone()[0]
        conn.close()
        return count > 0

    @staticmethod
    def create_admin(username, password):
        """Create new admin"""
        hashed_password = hash_password(password)
        
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO Admin (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()