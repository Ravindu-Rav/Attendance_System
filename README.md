# Face Recognition Attendance System

A desktop attendance system that uses face recognition to check employees in and out, built with Python, OpenCV, SQLite, and a PySide6 GUI.

## Features

- Admin login and first-time admin registration
- Employee management (add, edit, delete)
- Face capture per employee with dataset storage
- Model training (LBPH) and automatic model reload during scanning
- Check-in and check-out modes with early-leave approval flow
- Dashboard with attendance stats, trends, and department overview
- Attendance records table with CSV export

## Tech Stack

- Python
- OpenCV + OpenCV Contrib (LBPH face recognizer)
- PySide6 (GUI)
- SQLite
- NumPy

## Project Structure

```
app/
  main.py                      # CLI entry point (menu-based)
  config/settings.py           # App settings
  controllers/
    auth_controller.py
    attendance_controller.py
    registration_controller.py
    training_controller.py
  database/db.py               # SQLite init + connection
  models/
    admin_repository.py
    employee_repository.py
  presentation/gui/
    login_window.py
    admin_registration_window.py
    main_window.py
    dashboard_window.py
    employee_window.py
    attendance_window.py
    training_window.py
  services/
    attendance_logic_service.py
    attendance_service.py
    dashboard_service.py
    face_recognition_service.py
    registration_service.py
    training_service.py
  utils/password_utils.py
dataset/                        # Face image folders per employee ID
models_storage/                 # Trained model files
attendance.db                   # SQLite database
run.py                          # GUI entry point
requirements.txt
```

## Prerequisites

- Python (compatible with PySide6 6.7)
- A working webcam
- Windows, macOS, or Linux with OpenCV-compatible camera drivers

## Installation

1. Clone the repository

```bash
git clone <repository-url>
cd Attendance_System
```

2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

Windows CMD:

```bash
.\venv\Scripts\activate.bat
```

Linux/macOS:

```bash
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the App

### GUI (recommended)

```bash
python run.py
```

On first launch, use the "Create one" link on the login screen to register the first admin. After that, log in to access the main menu.

### CLI (menu-based)

```bash
python app/main.py
```

The CLI menu supports employee registration, model training, attendance marking, and admin registration. If PySide6 is installed, it also offers an option to launch the GUI.

## Typical Workflow

1. Register the first admin.
2. Add employees from the GUI.
3. Capture face samples for each employee.
4. Train the recognition model.
5. Use Check-In / Check-Out scanning to mark attendance.

## Attendance Rules (GUI)

- Workday start: 08:00
- Workday end: 16:00
- Check-out before completing 8 hours requires admin approval
- Approvals are handled in the Dashboard > Admin panel

## Data Storage

- `attendance.db` stores employees, departments, attendance records, and admins.
- `dataset/` stores face images per employee ID.
- `models_storage/trainer.yml` stores the trained LBPH model.

## Configuration

Key settings live in `app/config/settings.py`, including:

- `DATASET_DIR`
- `MODEL_PATH`
- `FACE_RECOGNITION_CONFIDENCE_THRESHOLD`
- `CAMERA_INDEX`

## Troubleshooting

- Camera not detected: make sure the webcam is connected and not in use by another app.
- "Model not trained": capture faces for employees and run training.
- Database locked: close other running instances of the app.
- Import errors: ensure you run from the project root and install requirements.

## License

This project is for educational purposes.

