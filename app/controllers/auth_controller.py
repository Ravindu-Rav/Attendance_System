"""Authentication Controller"""
from app.models.admin_repository import AdminRepository


def authenticate_admin(username, password):
    """Authenticate admin user"""
    if not username or not password:
        raise ValueError("Username and password are required")
    
    admin = AdminRepository.get_admin_by_credentials(username, password)
    return admin is not None


def register_admin(username, password, confirm_password):
    """Register new admin account"""
    if not username or not password:
        raise ValueError("Username and password cannot be empty.")
    
    if password != confirm_password:
        raise ValueError("Passwords do not match.")
    
    # Check if admin already exists
    if AdminRepository.admin_exists():
        raise ValueError("Admin account already exists.")
    
    AdminRepository.create_admin(username, password)