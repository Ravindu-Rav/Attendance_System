import cv2
import sqlite3
from datetime import datetime

DB_NAME = "attendance.db"


def get_employee(employee_id):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT fname, lname FROM Employee WHERE employee_ID=?
    """, (employee_id,))

    row = c.fetchone()

    conn.close()

    return row


def mark_attendance(employee_id):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    c.execute("""
    SELECT * FROM On_Duty 
    WHERE employee_ID=? AND date=?
    """, (employee_id, today))

    already_marked = c.fetchone()

    if already_marked is None:

        c.execute("""
        INSERT INTO On_Duty(employee_ID, duration, date)
        VALUES(?, ?, ?)
        """, (employee_id, 8, today))

        conn.commit()
        print("Attendance recorded.")

    else:
        print("Attendance already marked today.")

    conn.close()


def main():

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cam = cv2.VideoCapture(0)

    print("Starting face recognition...")

    while True:

        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            face = gray[y:y+h, x:x+w]

            employee_id, confidence = recognizer.predict(face)

            if confidence < 60:

                employee = get_employee(employee_id)

                if employee:

                    name = employee[0] + " " + employee[1]

                    cv2.putText(img, name,
                                (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1,
                                (0, 255, 0),
                                2)

                    mark_attendance(employee_id)

            else:

                cv2.putText(img, "Unknown",
                            (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            2)

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Face Attendance Scanner", img)

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

#Open webcam

#Detect a face using OpenCV

#Recognize the employee using trainer.yml

#Retrieve employee info from SQLite

#Record attendance in On_Duty table.