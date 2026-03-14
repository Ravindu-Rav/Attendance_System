"""Attendance System - Main Entry Point"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from app.presentation.gui.login_window import LoginWindow
    from app.database.db import init_db
    
    # Initialize database
    init_db()
    
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showFullScreen()
    sys.exit(app.exec())
