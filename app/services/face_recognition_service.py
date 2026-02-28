"""Face Recognition and Attendance Service"""
import cv2
from datetime import datetime
from app.database.db import get_connection
from app.config.settings import MODEL_PATH


def get_employee_name(employee_id):
    """Get employee name from database
    
    Args:
        employee_id: Employee ID
    
    Returns:
        Tuple of (first_name, last_name) or None
    """
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    SELECT fname, lname FROM Employee WHERE employee_ID=?
    """, (employee_id,))

    row = c.fetchone()
    conn.close()

    return row


def is_attendance_marked_today(employee_id):
    """Check if attendance already marked for today
    
    Args:
        employee_id: Employee ID
    
    Returns:
        True if already marked, False otherwise
    """
    conn = get_connection()
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("""
    SELECT * FROM On_Duty 
    WHERE employee_ID=? AND date=?
    """, (employee_id, today))

    result = c.fetchone() is not None
    conn.close()

    return result


def mark_attendance(employee_id):
    """Mark attendance for employee
    
    Args:
        employee_id: Employee ID
    
    Returns:
        True if marked successfully, False if already marked
    """
    if is_attendance_marked_today(employee_id):
        return False

    conn = get_connection()
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("""
    INSERT INTO On_Duty(employee_ID, duration, date)
    VALUES(?, ?, ?)
    """, (employee_id, 8, today))

    conn.commit()
    conn.close()
    return True


def start_face_recognition(confidence_threshold=60):
    """Start face recognition and attendance marking
    
    Args:
        confidence_threshold: Confidence threshold for recognition (lower = more strict)
    """
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cam = cv2.VideoCapture(0)

    print("Starting face recognition...")
    print("Press ESC to quit")

    while True:
        ret, img = cam.read()
        if not ret:
            print("Failed to capture frame")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            employee_id, confidence = recognizer.predict(face)

            if confidence < confidence_threshold:
                employee = get_employee_name(employee_id)

                if employee:
                    name = f"{employee[0]} {employee[1]}"
                    marked = mark_attendance(employee_id)
                    status = "✓ Marked" if marked else "Already Marked"

                    cv2.putText(img, f"{name} ({status})",
                                (x, y - 30),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.8,
                                (0, 255, 0),
                                2)
                    cv2.putText(img, f"Conf: {confidence:.2f}",
                                (x, y - 5),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                (0, 255, 0),
                                1)

            else:
                cv2.putText(img, f"Unknown (Conf: {confidence:.2f})",
                            (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 0, 255),
                            2)

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Face Attendance Scanner - Press ESC to quit", img)

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    print("Face recognition stopped")
