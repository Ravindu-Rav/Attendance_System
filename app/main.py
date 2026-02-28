"""Main entry point for Attendance System"""
from app.database.db import init_db
from app.controllers.registration_controller import handle_register_employee
from app.controllers.attendance_controller import handle_mark_attendance
from app.controllers.training_controller import handle_train_model


def show_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("        ATTENDANCE SYSTEM MENU")
    print("="*50)
    print("1. Register Employee")
    print("2. Train Model")
    print("3. Mark Attendance")
    print("4. Exit")
    print("="*50)


def main():
    """Main application loop"""
    init_db()
    
    while True:
        show_menu()
        choice = input("Select an option (1-4): ").strip()
        
        if choice == "1":
            handle_register_employee()
        elif choice == "2":
            handle_train_model()
        elif choice == "3":
            handle_mark_attendance()
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()