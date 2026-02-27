# Face Recognition Attendance System

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.x-orange.svg)](https://www.sqlite.org/)

An intelligent attendance management system using **Python**, **OpenCV**, and **SQLite**. Employees mark attendance via facial recognition through a laptop webcam. Admins manage employees, capture photos, and monitor attendance logs.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Features

### Admin Functionality

- ➕ Add new employees with basic details (name, age)
- 📸 Capture multiple face images via webcam
- 📊 View attendance records with employee details

### Employee Functionality

- 🔍 Scan face using webcam to mark attendance
- 📝 Attendance automatically logged in the database

### Database

- 🗄️ SQLite database for employees, attendance logs, and admin credentials
- 🔒 No external dependencies for storage

### Face Recognition

- 🤖 Uses OpenCV LBPHFaceRecognizer
- 📷 Multiple images per employee for higher accuracy
- ⚡ Real-time recognition with webcam

## Tech Stack

- **Python** 3.x
- **OpenCV** (`cv2`)
- **SQLite** (`sqlite3`)
- **Optional GUI**: PySide6 or Tkinter

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
# Activate the environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install opencv-python opencv-contrib-python numpy
# For GUI (optional)
pip install PySide6
```

### 4. Database Setup

The project automatically creates `attendance.db` on first run with the following tables:

- `admin` - Admin credentials
- `employees` - Employee details
- `attendance` - Attendance logs

### 5. Run the Application

- Launch the admin login GUI or use the command-line version
- Admin workflow: Add employees → Capture photos → Train face recognizer
- Employee workflow: Scan face → Mark attendance

## Project Structure

```
face-attendance-system/
│
├── employee_photos/          # 📁 Captured employee face images
├── attendance.db             # 🗄️ SQLite database
├── main.py                   # 🚀 Main script to run the app
├── capture_photos.py         # 📸 Capture employee photos
├── train_recognizer.py       # 🧠 Train face recognizer
├── mark_attendance.py        # ✅ Mark attendance
└── README.md                 # 📖 This file
```

## Usage

### 1. Add Employee (Admin)

- Provide employee name and age
- Capture 20 face photos via webcam for training

### 2. Train Recognizer

- Run `train_recognizer.py` after adding employees
- Generates `face_trainer.yml` for recognition

### 3. Mark Attendance (Employee)

- Execute `mark_attendance.py`
- Face scan triggers automatic attendance logging

### 4. View Attendance (Admin)

- Query the database or use GUI for attendance history

## Future Enhancements

- 🔄 Replace LBPH with advanced Face Recognition library for better accuracy
- 🖥️ Implement GUI for both Admin and Employee interfaces
- 📈 Export attendance logs to CSV or Excel
- 👥 Enable multi-face detection
- 🔐 Add password hashing for Admin login security

## License

This project is open-source and free to use for learning purposes. 📚
