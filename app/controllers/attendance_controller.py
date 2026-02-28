"""Attendance Controller"""
from app.services.face_recognition_service import start_face_recognition


def handle_mark_attendance():
    """Handle attendance marking workflow"""
    try:
        start_face_recognition(confidence_threshold=60)
    except Exception as e:
        print(f"Error during attendance marking: {e}")
