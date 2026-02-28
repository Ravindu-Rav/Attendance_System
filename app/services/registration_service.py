"""Employee Registration Service"""
import cv2
import os
from app.database.db import get_connection
from app.config.settings import DATASET_DIR


def add_employee(fname, lname, gender, age, email, password):
    """Add new employee to database
    
    Args:
        fname: First name
        lname: Last name
        gender: Gender (1=Male, 2=Female)
        age: Age
        email: Email address
        password: Password
    
    Returns:
        Employee ID
    """
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    INSERT INTO Employee (fname, lname, gender, age, emp_email, emp_pass)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (fname, lname, gender, age, email, password))

    employee_id = c.lastrowid
    conn.commit()
    conn.close()

    return employee_id


def capture_faces(employee_id, num_samples=30):
    """Capture face images for employee
    
    Args:
        employee_id: Employee ID
        num_samples: Number of face samples to capture (default: 30)
    """
    dataset_path = os.path.join(DATASET_DIR, str(employee_id))
    os.makedirs(dataset_path, exist_ok=True)

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cam = cv2.VideoCapture(0)
    count = 0

    print(f"Capturing {num_samples} face samples for employee {employee_id}")
    print("Press ESC to quit")

    while True:
        ret, img = cam.read()
        if not ret:
            print("Failed to capture frame")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face = gray[y:y+h, x:x+w]
            file_path = os.path.join(dataset_path, f"{count}.jpg")
            cv2.imwrite(file_path, face)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(img, f"Samples: {count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Capturing Faces - Press ESC to quit", img)

        if cv2.waitKey(1) == 27 or count >= num_samples:
            break

    cam.release()
    cv2.destroyAllWindows()
    print(f"Face dataset created with {count} samples")


def register_employee_with_photos():
    """Interactive employee registration with photo capture"""
    fname = input("First Name: ")
    lname = input("Last Name: ")
    gender = int(input("Gender (1=Male, 2=Female): "))
    age = int(input("Age: "))
    email = input("Email: ")
    password = input("Password: ")

    employee_id = add_employee(fname, lname, gender, age, email, password)
    print(f"Employee created with ID: {employee_id}")

    capture_faces(employee_id)
    print("Registration complete!")
