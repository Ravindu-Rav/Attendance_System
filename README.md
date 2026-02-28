# Attendance System

A face recognition-based employee attendance system using OpenCV and SQLite.

## Features

- **Employee Registration**: Register new employees with face capture
- **Face Recognition**: Real-time face recognition for attendance marking
- **Model Training**: Train the recognition model with employee photos
- **Attendance Tracking**: Automatic attendance marking via face recognition
- **Modular Architecture**: Clean separation of concerns with services, controllers, and models

## Project Structure

\\\
Attendance_System/
+-- app/                          # Main application package
¦   +-- __init__.py
¦   +-- main.py                   # Main entry point with menu
¦   +-- config/                   # Configuration
¦   ¦   +-- __init__.py
¦   ¦   +-- settings.py           # App settings (DB, paths)
¦   +-- database/                 # Database layer
¦   ¦   +-- __init__.py
¦   ¦   +-- db.py                 # Database connection & init
¦   +-- models/                   # Data models
¦   ¦   +-- __init__.py
¦   ¦   +-- employee.py           # Employee model
¦   +-- services/                 # Business logic
¦   ¦   +-- __init__.py
¦   ¦   +-- registration_service.py      # Employee registration
¦   ¦   +-- face_recognition_service.py  # Face recognition & attendance
¦   ¦   +-- training_service.py          # Model training
¦   ¦   +-- attendance_service.py        # Attendance operations
¦   +-- controllers/              # Request handlers
¦   ¦   +-- __init__.py
¦   ¦   +-- registration_controller.py   # Register workflow
¦   ¦   +-- attendance_controller.py     # Attendance workflow
¦   ¦   +-- training_controller.py       # Training workflow
¦   +-- utils/                    # Utilities
¦       +-- __init__.py
+-- dataset/                      # Employee face photos directory
+-- db/                           # Database files
+-- employee_photos/              # Employee photos storage
+-- models_storage/               # Trained model storage
+-- run.py                        # Main entry point
+-- requirements.txt              # Python dependencies
+-- README.md                     # This file
\\\

## Prerequisites

- Python 3.7 or higher
- Webcam/Camera device
- SQLite3 (included with Python)

## Installation

1. Create a virtual environment:
   \\\ash
   python -m venv .venv
   \\\

2. Activate the virtual environment:
   - Windows PowerShell:
     \\\powershell
     .\\.venv\\Scripts\\Activate.ps1
     \\\
   - Windows CMD:
     \\\cmd
     .\\.venv\\Scripts\\activate.bat
     \\\
   - Linux/Mac:
     \\\ash
     source .venv/bin/activate
     \\\

3. Install dependencies:
   \\\ash
   pip install -r requirements.txt
   \\\

## Usage

1. Run the application:
   \\\ash
   python run.py
   \\\

2. Follow the menu:
   - **Option 1**: Register a new employee
     - Enter employee details (name, age, email, etc.)
     - Capture face samples (30 images per employee)
   
   - **Option 2**: Train the model
     - Trains face recognizer with all captured photos
     - Saves model as \models_storage/trainer.yml\
   
   - **Option 3**: Mark attendance
     - Starts real-time face recognition
     - Automatically marks attendance for recognized employees
     - Press ESC to exit

## Module Descriptions

### Services
- **registration_service.py**: Employee registration and face capture
- **face_recognition_service.py**: Face recognition and attendance marking
- **training_service.py**: LBPH face recognizer model training
- **attendance_service.py**: Attendance database operations

### Controllers
- **registration_controller.py**: Registration workflow management
- **attendance_controller.py**: Attendance marking workflow
- **training_controller.py**: Model training workflow

### Database
- **db.py**: Database initialization and connection
- Tables: Employee, Department, Job_Title, On_Duty

### Configuration
- **settings.py**: Centralized app configuration

## Key Improvements

? Modular architecture (services, controllers, models)
? Centralized configuration management
? Proper package structure with \__init__.py\
? Clean separation of concerns
? Comprehensive error handling
? Clear documentation

## Notes

- Minimum 5-8 employees needed for best accuracy
- Each employee should have 20-30 face samples
- Confidence threshold: 60 (adjustable)
- Database file: \ttendance.db\
- Trained model: \models_storage/trainer.yml\

## Troubleshooting

- **Camera not detected**: Ensure webcam is connected
- **"Unknown" faces**: Retrain model with better lighting
- **Module errors**: Run from project root directory
- **Database locked**: Close other app instances

## Dependencies

- opencv-python: Image processing
- opencv-contrib-python: LBPH recognizer
- numpy: Numerical operations
