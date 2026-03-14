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

├── app/ # Main application package
│ ├── **init**.py
│ ├── main.py # CLI main entry point with menu
│ ├── config/ # Configuration
│ │ ├── **init**.py
│ │ └── settings.py # App settings (DB, paths)
│ ├── database/ # Database layer
│ │ ├── **init**.py
│ │ └── db.py # Database connection & init
│ ├── models/ # Data models
│ │ ├── **init**.py
│ │ ├── employee.py # Employee model
│ │ └── admin.py # Admin model
│ ├── services/ # Business logic
│ │ ├── **init**.py
│ │ ├── registration_service.py # Employee registration
│ │ ├── face_recognition_service.py # Face recognition & attendance
│ │ ├── training_service.py # Model training
│ │ └── attendance_service.py # Attendance operations
│ ├── controllers/ # Request handlers
│ │ ├── **init**.py
│ │ ├── registration_controller.py # Register workflow
│ │ ├── attendance_controller.py # Attendance workflow
│ │ └── training_controller.py # Training workflow
│ └── presentation/ # GUI layer
│ └── gui/ # Graphical user interface
│ ├── **init**.py
│ ├── login_window.py # Admin login
│ ├── admin_registration_window.py # Admin registration
│ ├── main_window.py # Main menu
│ ├── dashboard_window.py # Dashboard
│ ├── employee_window.py # Employee management
│ ├── attendance_window.py # Attendance marking
│ └── training_window.py # Model training
├── dataset/ # Employee face photos directory
├── models_storage/ # Trained model storage
├── run.py # GUI main entry point
├── requirements.txt # Python dependencies
└── README.md # This file

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

### Initial Setup

#### 1. Register Admin Account

Before using the system, you need to create an admin account:

```bash
python run.py
```

Select option **4** to register the first admin account. This is required for system access.

### GUI Application

The system includes a modern GUI interface for easier management:

#### Run the GUI Application

```bash
python run.py
```

Select option **5** to launch the GUI application.

#### GUI Features

- **Admin Login**: Secure login for administrators
- **Dashboard**: View attendance statistics and system overview
- **Employee Management**: Add, edit, and manage employee records
- **Attendance Marking**: Real-time face recognition attendance
- **Model Training**: Train the face recognition model with GUI progress
- **Admin Registration**: Create admin accounts (first-time setup)

### Admin Registration

The system requires at least one admin account for access. To register the first admin:

1. Run `python run.py`
2. Select option **4** (Register Admin)
3. Enter a username and password
4. The admin account will be created

For GUI registration:

1. Run `python run.py`
2. Select option **5** (Launch GUI)
3. If no admin exists, click "Register Admin" link on the login screen
4. Fill in the registration form

**Note**: Admin registration is only available when no admin accounts exist in the system.

### CLI Menu Options

| Option | Action            | Description                                     |
| ------ | ----------------- | ----------------------------------------------- |
| **1**  | Register Employee | Enter details and capture 30 face samples       |
| **2**  | Train Model       | Train face recognizer with all photos           |
| **3**  | Mark Attendance   | Start real-time recognition (Press ESC to exit) |
| **4**  | Register Admin    | Create admin account for system access          |
| **5**  | Launch GUI        | Start the graphical user interface              |

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
