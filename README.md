# 🎯 Face Recognition Attendance System

A modern face recognition-based employee attendance system built with Python, OpenCV, and SQLite.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)

---

## ✨ Features

| Feature                      | Description                                                         |
| ---------------------------- | ------------------------------------------------------------------- |
| 👤 **Employee Registration** | Register new employees with face capture                            |
| 🔐 **Face Recognition**      | Real-time face recognition for attendance marking                   |
| 🧠 **Model Training**        | Train the recognition model with employee photos                    |
| 📊 **Attendance Tracking**   | Automatic attendance marking via face recognition                   |
| 🏗️ **Modular Architecture**  | Clean separation of concerns with services, controllers, and models |

---

## 📁 Project Structure

```
Attendance_System/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # Main entry point with menu
│   ├── config/                   # Configuration
│   │   ├── __init__.py
│   │   └── settings.py           # App settings (DB, paths)
│   ├── database/                 # Database layer
│   │   ├── __init__.py
│   │   └── db.py                 # Database connection & init
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   └── employee.py           # Employee model
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── registration_service.py      # Employee registration
│   │   ├── face_recognition_service.py  # Face recognition & attendance
│   │   ├── training_service.py          # Model training
│   │   └── attendance_service.py        # Attendance operations
│   ├── controllers/              # Request handlers
│   │   ├── __init__.py
│   │   ├── registration_controller.py   # Register workflow
│   │   ├── attendance_controller.py     # Attendance workflow
│   │   └── training_controller.py        # Training workflow
│   └── utils/                    # Utilities
│       └── __init__.py
├── dataset/                      # Employee face photos directory
├── models_storage/               # Trained model storage
├── run.py                        # Main entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🛠️ Prerequisites

- **Python**: 3.7 or higher
- **Camera**: Webcam or external camera device
- **SQLite**: Included with Python

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Attendance_System
```

### 2. Create a virtual environment

```
bash
python -m venv venv
```

### 3. Activate the virtual environment

| OS                       | Command                       |
| ------------------------ | ----------------------------- |
| **Windows (PowerShell)** | `.\venv\Scripts\Activate.ps1` |
| **Windows (CMD)**        | `.\venv\Scripts\activate.bat` |
| **Linux/Mac**            | `source venv/bin/activate`    |

### 4. Install dependencies

```
bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run the application

```
bash
python run.py
```

### Menu Options

| Option | Action            | Description                                     |
| ------ | ----------------- | ----------------------------------------------- |
| **1**  | Register Employee | Enter details and capture 30 face samples       |
| **2**  | Train Model       | Train face recognizer with all photos           |
| **3**  | Mark Attendance   | Start real-time recognition (Press ESC to exit) |

---

## 📋 Module Descriptions

### Services

| Module                        | Purpose                                 |
| ----------------------------- | --------------------------------------- |
| `registration_service.py`     | Employee registration and face capture  |
| `face_recognition_service.py` | Face recognition and attendance marking |
| `training_service.py`         | LBPH face recognizer model training     |
| `attendance_service.py`       | Attendance database operations          |

### Controllers

| Module                       | Purpose                          |
| ---------------------------- | -------------------------------- |
| `registration_controller.py` | Registration workflow management |
| `attendance_controller.py`   | Attendance marking workflow      |
| `training_controller.py`     | Model training workflow          |

### Database

- **db.py**: Database initialization and connection
- **Tables**: Employee, Department, Job_Title, On_Duty

### Configuration

- **settings.py**: Centralized app configuration

---

## ⚙️ Configuration Notes

| Setting                        | Value                        |
| ------------------------------ | ---------------------------- |
| Minimum employees for training | 5-8                          |
| Face samples per employee      | 20-30                        |
| Confidence threshold           | 60 (adjustable)              |
| Database file                  | `attendance.db`              |
| Trained model                  | `models_storage/trainer.yml` |

---

## 🔧 Troubleshooting

| Issue               | Solution                                      |
| ------------------- | --------------------------------------------- |
| Camera not detected | Ensure webcam is connected and working        |
| "Unknown" faces     | Retrain model with better lighting conditions |
| Module errors       | Run from project root directory               |
| Database locked     | Close other application instances             |

---

## 📚 Dependencies

- **opencv-python**: Image processing
- **opencv-contrib-python**: LBPH face recognizer
- **numpy**: Numerical operations
- **pillow**: Image handling

---

## 📝 License

This project is for educational purposes.

---

_Built with ❤️ using Python and OpenCV_
