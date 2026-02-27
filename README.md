---
# Face Recognition Attendance System

An ** attendance system** using **Python**, **OpenCV**, and **SQLite**, with **admin and employee management**. Employees can mark attendance using their face via a laptop webcam. Admins can add employees, capture their photos, and view attendance logs.
---

## **Features**

- **Admin functionality**
  - Add new employees with basic details (name, age)
  - Capture multiple face images of employees via webcam
  - View attendance records with employee details

- **Employee functionality**
  - Scan face using webcam to mark attendance
  - Attendance is automatically logged in the database

- **Database**
  - SQLite database stores employees, attendance logs, and admin credentials
  - No external dependencies for storage

- **Face Recognition**
  - Uses **OpenCV LBPHFaceRecognizer**
  - Multiple images per employee for higher accuracy
  - Real-time recognition with webcam

---

## **Tech Stack**

- Python 3.x
- OpenCV (`cv2`)
- SQLite (`sqlite3`)
- Optional GUI: PySide6 or Tkinter

---

## **Setup Instructions**

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install opencv-python opencv-contrib-python numpy
# For GUI (optional)
pip install PySide6
```

4. **Create SQLite database**

The project will automatically create `attendance.db` when first run, with tables:

- `admin`
- `employees`
- `attendance`

5. **Run the application**

- Start with the **admin login GUI** or a command-line version
- Admin can add employees → capture photos → train face recognizer
- Employees can scan face → mark attendance

---

## **Project Structure**

```
face-attendance-system/
│
├─ employee_photos/          # Captured employee face images
├─ attendance.db             # SQLite database
├─ main.py                   # Main script to run the app
├─ capture_photos.py         # Capture employee photos
├─ train_recognizer.py       # Train face recognizer
├─ mark_attendance.py        # Mark attendance
└─ README.md
```

---

## **Usage**

1. **Add Employee (Admin)**
   - Provide name and age
   - Capture 20 face photos via webcam

2. **Train Recognizer**
   - Run `train_recognizer.py` after adding employees
   - Saves `face_trainer.yml` for recognition

3. **Mark Attendance (Employee)**
   - Run `mark_attendance.py`
   - Face is scanned and attendance logged automatically

4. **View Attendance (Admin)**
   - Admin can query the database or use GUI to see attendance history

---

## **Future Enhancements**

- Replace LBPH with **Face Recognition library** for higher accuracy
- Add GUI for both Admin and Employee
- Export attendance logs to **CSV** or **Excel**
- Implement **multi-face detection**
- Add **password hashing** for Admin login

---

## **License**

This project is open-source and free to use for learning purposes.

---
