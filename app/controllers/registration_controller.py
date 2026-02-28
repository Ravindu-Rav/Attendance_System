"""Registration Controller"""
from app.services.registration_service import (
    register_employee_with_photos,
    add_employee,
    capture_faces
)


def handle_register_employee():
    """Handle employee registration workflow"""
    try:
        register_employee_with_photos()
    except Exception as e:
        print(f"Error during registration: {e}")
