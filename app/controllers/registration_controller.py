"""Registration Controller"""
from app.services.registration_service import (
    register_employee_with_photos,
    capture_faces
)
from app.models.employee_repository import EmployeeRepository


def handle_register_employee():
    """Handle employee registration workflow"""
    try:
        register_employee_with_photos()
    except Exception as e:
        print(f"Error during registration: {e}")


def handle_add_employee(name, employee_id, department=None):
    """Add new employee"""
    if not name or not employee_id:
        raise ValueError("Name and Employee ID are required")
    
    # Split name
    parts = name.split()
    fname = parts[0]
    lname = ' '.join(parts[1:]) if len(parts) > 1 else ''
    
    from app.services.registration_service import add_employee
    return add_employee(int(employee_id), fname, lname, dept_id=department)


def handle_capture_faces(employee_id, num_samples=50):
    """Capture faces for employee"""
    if not employee_id:
        raise ValueError("Employee ID is required")
    capture_faces(employee_id, num_samples)


def handle_get_employees():
    """Get all employees"""
    return EmployeeRepository.get_all_employees()


def handle_update_employee(employee_id, name):
    """Update employee name"""
    if not name:
        raise ValueError("Name is required")
    
    parts = name.split()
    fname = parts[0]
    lname = ' '.join(parts[1:]) if len(parts) > 1 else ''
    
    EmployeeRepository.update_employee(employee_id, fname, lname)


def handle_delete_employee(employee_id):
    """Delete employee"""
    EmployeeRepository.delete_employee(employee_id)
