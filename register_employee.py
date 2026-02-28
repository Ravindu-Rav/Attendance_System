import sqlite3
import cv2
import os

DB_NAME = "attendance.db"


def add_employee(fname, lname, gender, age, email, password):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO Employee (fname, lname, gender, age, emp_email, emp_pass)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (fname, lname, gender, age, email, password))

    employee_id = c.lastrowid

    conn.commit()
    conn.close()

    return employee_id


def capture_faces(employee_id):

    dataset_path = f"dataset/{employee_id}"
    os.makedirs(dataset_path, exist_ok=True)

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cam = cv2.VideoCapture(0)

    count = 0

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1

            face = gray[y:y+h, x:x+w]

            file_path = f"{dataset_path}/{count}.jpg"
            cv2.imwrite(file_path, face)

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

        cv2.imshow("Capturing Faces", img)

        if cv2.waitKey(1) == 27 or count >= 30:
            break

    cam.release()
    cv2.destroyAllWindows()

    print("Face dataset created.")


def main():

    fname = input("First Name: ")
    lname = input("Last Name: ")
    gender = int(input("Gender (1=Male,2=Female): "))
    age = int(input("Age: "))
    email = input("Email: ")
    password = input("Password: ")

    employee_id = add_employee(fname, lname, gender, age, email, password)

    print(f"Employee created with ID: {employee_id}")

    capture_faces(employee_id)


if __name__ == "__main__":
    main()