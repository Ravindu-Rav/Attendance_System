"""Main entry point for Attendance System"""
from app.database.db import init_db
from app.controllers.registration_controller import handle_register_employee
from app.controllers.attendance_controller import handle_mark_attendance
from app.controllers.training_controller import handle_train_model
import sys
import os

# Add GUI imports
try:
    from PySide6.QtWidgets import QApplication
    from app.presentation.gui.login_window import LoginWindow
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


def show_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("        ATTENDANCE SYSTEM MENU")
    print("="*50)
    print("1. Register Employee")
    print("2. Train Model")
    print("3. Mark Attendance")
    print("4. Register Admin")
    if GUI_AVAILABLE:
        print("5. Launch GUI")
        print("6. Exit")
    else:
        print("5. Exit")
    print("="*50)


def handle_register_admin():
    """Handle admin registration"""
    print("\n--- Admin Registration ---")
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()
    confirm_password = input("Confirm admin password: ").strip()
    
    if not username or not password:
        print("Username and password cannot be empty.")
        return
    
    if password != confirm_password:
        print("Passwords do not match.")
        return
    
    # Import here to avoid circular imports
    from app.database.db import get_connection
    import hashlib
    
    conn = get_connection()
    c = conn.cursor()
    
    # Check if admin already exists
    c.execute("SELECT COUNT(*) FROM Admin")
    if c.fetchone()[0] > 0:
        print("Admin account already exists. Only one admin registration allowed.")
        conn.close()
        return
    
    # Hash password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        c.execute("INSERT INTO Admin (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print(f"Admin account '{username}' created successfully!")
    except Exception as e:
        print(f"Error creating admin account: {e}")
    finally:
        conn.close()


def launch_gui():
    """Launch the GUI application"""
    if not GUI_AVAILABLE:
        print("GUI not available. Please install PySide6.")
        return
    
    print("Launching GUI...")
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())


def main():
    """Main application loop"""
    init_db()
    
    while True:
        show_menu()
        if GUI_AVAILABLE:
            choice = input("Select an option (1-6): ").strip()
        else:
            choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            handle_register_employee()
        elif choice == "2":
            handle_train_model()
        elif choice == "3":
            handle_mark_attendance()
        elif choice == "4":
            handle_register_admin()
        elif choice == "5" and GUI_AVAILABLE:
            launch_gui()
        elif (choice == "5" and not GUI_AVAILABLE) or (choice == "6" and GUI_AVAILABLE):
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()