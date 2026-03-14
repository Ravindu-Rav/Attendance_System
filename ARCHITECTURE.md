# High-Level Architecture Diagram Details

## Face Recognition Attendance System

---

## 1. SYSTEM OVERVIEW

The Attendance System is a Python-based face recognition application built with a **Layered Architecture (MVC-inspired)** pattern.

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                          │
│                    (GUI - PySide6)                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────┐│
│  │  Login   │ │  Main    │ │Dashboard │ │Employee  │ │Attend.││
│  │ Window   │ │ Window   │ │ Window   │ │ Window   │ │Window ││
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └───────┘│
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────┐
│                    CONTROLLER LAYER                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│  │ Registration │ │  Attendance  │ │  Training    │             │
│  │ Controller   │ │  Controller  │ │  Controller  │             │
│  └──────────────┘ └──────────────┘ └──────────────┘             │
└──────────────────────────┼──────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────┐
│                    SERVICE LAYER (Business Logic)              │
│  ┌──────────────────┐ ┌──────────────────┐ ┌───────────────┐    │
│  │ Registration     │ │ Face Recognition │ │   Training    │    │
│  │ Service          │ │ Service          │ │   Service     │    │
│  │ - add_employee   │ │ - start_face_   │ │ - train_model │    │
│  │ - capture_faces  │ │   recognition    │ │ - get_images │    │
│  │                  │ │ - mark_attendance│ │   _and_labels│    │
│  └──────────────────┘ └──────────────────┘ └───────────────┘    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Attendance Service                             ││
│  │              - mark_attendance                              ││
│  └─────────────────────────────────────────────────────────────┘│
└──────────────────────────┼──────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────┐
│                      DATA LAYER                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐    │
│  │   Database     │  │    Models       │  │   Config      │    │
│  │   (SQLite)     │  │   (Employee)    │  │  (Settings)   │    │
│  │ - Employee     │  │ - employee_id   │  │ - DB_PATH     │    │
│  │ - Department   │  │ - fname         │  │ - DATASET_DIR │    │
│  │ - Job_Title    │  │ - lname         │  │ - MODEL_PATH  │    │
│  │ - On_Duty      │  │ - email         │  │               │    │
│  └─────────────────┘  └─────────────────┘  └───────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. LAYER DETAILS

### 2.1 PRESENTATION LAYER (GUI - PySide6)

| Component        | File                   | Purpose                      |
| ---------------- | ---------------------- | ---------------------------- |
| LoginWindow      | `login_window.py`      | User authentication UI       |
| MainWindow       | `main_window.py`       | Main application container   |
| DashboardWindow  | `dashboard_window.py`  | Dashboard display            |
| EmployeeWindow   | `employee_window.py`   | Employee management UI       |
| AttendanceWindow | `attendance_window.py` | Attendance marking interface |

### 2.2 CONTROLLER LAYER

| Controller             | File                         | Responsibilities                            |
| ---------------------- | ---------------------------- | ------------------------------------------- |
| RegistrationController | `registration_controller.py` | Orchestrates employee registration workflow |
| AttendanceController   | `attendance_controller.py`   | Manages attendance marking process          |
| TrainingController     | `training_controller.py`     | Handles model training workflow             |

### 2.3 SERVICE LAYER

| Service                | File                          | Key Functions                                                                                  |
| ---------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------- |
| RegistrationService    | `registration_service.py`     | add_employee(), capture_faces(), register_employee_with_photos()                               |
| FaceRecognitionService | `face_recognition_service.py` | start_face_recognition(), mark_attendance(), get_employee_name(), is_attendance_marked_today() |
| TrainingService        | `training_service.py`         | train_model(), get_images_and_labels()                                                         |
| AttendanceService      | `attendance_service.py`       | mark_attendance()                                                                              |

### 2.4 DATA LAYER

| Component      | File          | Description                        |
| -------------- | ------------- | ---------------------------------- |
| Database       | `db.py`       | SQLite connection & initialization |
| Employee Model | `employee.py` | Employee data class                |
| Settings       | `settings.py` | Configuration constants            |

---

## 3. DATA FLOW DIAGRAMS

### 3.1 Employee Registration Flow

```
User Input → LoginWindow → RegistrationController → RegistrationService
                                                      ↓
                                            Database (Employee table)
                                                      ↓
                                            Camera → capture_faces()
                                                      ↓
                                            dataset/{employee_id}/
```

### 3.2 Attendance Marking Flow

```
User → AttendanceWindow → AttendanceController → FaceRecognitionService
                                                        ↓
                                              Camera (Real-time Video)
                                                        ↓
                                              OpenCV + LBPH Recognizer
                                                        ↓
                                              Model (trainer.yml)
                                                        ↓
                                              Match Found → Database (On_Duty)
                                                        ↓
                                              Attendance Confirmed
```

### 3.3 Model Training Flow

```
User → TrainingController → TrainingService
                                    ↓
                          dataset/ (all employees)
                                    ↓
                          get_images_and_labels()
                                    ↓
                          OpenCV LBPH Trainer
                                    ↓
                          models_storage/trainer.yml
```

---

## 4. DATABASE SCHEMA

```
┌─────────────────┐     ┌─────────────────┐
│   Department    │     │   Job_Title     │
├─────────────────┤     ├─────────────────┤
│ dept_ID (PK)   │     │ job_ID (PK)     │
│ department_name│     │ job_title       │
└─────────────────┘     │ dept_ID (FK)    │
                       │ employee_ID (FK)│
                       └────────┬────────┘
                                │
       ┌────────────────────────┼────────────────────────┐
       │                        │                        │
       ▼                        ▼                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Employee     │     │    On_Duty      │     │     (Config)    │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ employee_ID(PK)│     │ duty_ID (PK)    │     │ DATABASE_NAME   │
│ fname          │     │ employee_ID(FK) │     │ = "attendance.db"│
│ lname          │     │ job_ID (FK)     │     │                 │
│ gender         │     │ duration        │     │ DATASET_DIR     │
│ age            │     │ date            │     │ = "dataset"      │
│ contact_add    │     └─────────────────┘     │                 │
│ emp_email      │                             │ MODEL_PATH      │
│ emp_pass       │                             │ = "models_      │
└─────────────────┘                             │   storage/      │
                                                │   trainer.yml"  │
                                                └─────────────────┘
```

---

## 5. EXTERNAL COMPONENTS

```
┌────────────────────────────────────────────────────────────┐
│                 EXTERNAL COMPONENTS                        │
│                                                            │
│   ┌──────────────┐   ┌──────────────┐   ┌─────────────┐  │
│   │   OpenCV     │   │    NumPy     │   │   Camera    │  │
│   │  (cv2)       │   │              │   │  (Webcam)   │  │
│   │              │   │              │   │             │  │
│   │ - Face       │   │ - Array      │   │ - Video     │  │
│   │   Detection  │   │   Operations │   │   Capture   │  │
│   │ - LBPH       │   │ - Matrix     │   │ - Frames    │  │
│   │   Recognizer │   │   Math       │   │             │  │
│   └──────────────┘   └──────────────┘   └─────────────┘  │
│                                                            │
│   ┌─────────────────────────────────────────────────────┐ │
│   │              Haar Cascade Classifier              │ │
│   │         (haarcascade_frontalface_default.xml)     │ │
│   └─────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## 6. PROJECT STRUCTURE

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
│   ├── presentation/
│   │   └── gui/                  # GUI Windows
│   │       ├── login_window.py
│   │       ├── main_window.py
│   │       ├── dashboard_window.py
│   │       ├── employee_window.py
│   │       └── attendance_window.py
│   └── utils/                    # Utilities
│       └── __init__.py
├── dataset/                      # Employee face photos directory
├── models_storage/               # Trained model storage
├── run.py                        # Main entry point
├── requirements.txt              # Python dependencies
└── ARCHITECTURE.md               # This file
```

---

## 7. KEY TECHNOLOGIES

| Technology     | Version   | Purpose                      |
| -------------- | --------- | ---------------------------- |
| Python         | 3.7+      | Programming language         |
| OpenCV         | 4.8.1.78  | Face detection & recognition |
| OpenCV Contrib | 4.8.1.78  | LBPH Face Recognizer         |
| NumPy          | 1.24.3    | Numerical operations         |
| SQLite         | Built-in  | Local database               |
| PySide6        | (implied) | GUI framework                |

---

## 8. CONFIGURATION SETTINGS

| Setting              | Value                        | Description                                    |
| -------------------- | ---------------------------- | ---------------------------------------------- |
| DATABASE_NAME        | "attendance.db"              | SQLite database file                           |
| DATASET_DIR          | "dataset"                    | Directory for face images                      |
| MODEL_PATH           | "models_storage/trainer.yml" | Trained model file path                        |
| Confidence Threshold | 60                           | Face recognition confidence (lower = stricter) |
| Face Samples         | 20-30                        | Number of samples per employee                 |

---

## 9. CHALLENGES ENCOUNTERED

### 9.1 Technical Challenges

| Challenge                 | Description                                         | Potential Solutions                                                                                      |
| ------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Lighting Conditions**   | Face recognition accuracy degrades in poor lighting | Use consistent lighting, add infrared cameras, or implement image preprocessing (histogram equalization) |
| **Camera Quality**        | Low-resolution cameras may miss facial details      | Use HD cameras (720p+), ensure proper focus and distance                                                 |
| **Face Angle Variations** | Side angles or tilted faces are harder to detect    | Capture multiple angles during registration, use 3D face recognition                                     |
| **Performance Issues**    | Real-time processing may be slow on older hardware  | Optimize code, use GPU acceleration, reduce frame processing rate                                        |
| **Database Concurrency**  | Multiple users accessing SQLite simultaneously      | Implement connection pooling, consider PostgreSQL for scale                                              |
| **Model Training Time**   | Training with many employees takes long             | Batch processing, use faster algorithms, incremental learning                                            |

### 9.2 Implementation Challenges

| Challenge                     | Description                                             | Potential Solutions                                                  |
| ----------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------- |
| **Face Detection Failures**   | Haar cascade may not detect faces in certain conditions | Use dlib or MTCNN for better detection, combine multiple classifiers |
| **False Positives/Negatives** | Unknown people marked as employees or vice versa        | Adjust confidence threshold, improve training data quality           |
| **Image Storage**             | Large dataset of face images consumes storage           | Compress images, use face embeddings instead of raw images           |
| **Privacy Concerns**          | Storing facial data raises privacy issues               | Implement encryption, anonymization, comply with GDPR/local laws     |
| **Dependency Management**     | OpenCV version conflicts with other packages            | Use virtual environments, lock dependency versions                   |
| **Cross-Platform Issues**     | Code may behave differently on Windows/Mac/Linux        | Test on all platforms, use cross-platform libraries                  |

### 9.3 Operational Challenges

| Challenge                   | Description                                               | Potential Solutions                                           |
| --------------------------- | --------------------------------------------------------- | ------------------------------------------------------------- |
| **Employee Cooperation**    | Employees may not follow registration instructions        | Clear guidelines, visual guides, staff assistance             |
| **Multiple Face Detection** | System may struggle with multiple faces in frame          | Implement face tracking, queue system, or single-user mode    |
| **Anti-Spoofing**           | System can be fooled by photos/videos of authorized users | Implement liveness detection (blink, movement, depth sensors) |
| **Network Issues**          | If cloud-based components fail                            | Implement offline mode, local storage fallback                |
| **System Maintenance**      | Model retraining needed periodically                      | Automated retraining schedules, version control for models    |
| **User Adoption**           | Resistance to new technology                              | Training sessions, gradual rollout, demonstrate benefits      |

### 9.4 Security Challenges

| Challenge               | Description                        | Potential Solutions                                  |
| ----------------------- | ---------------------------------- | ---------------------------------------------------- |
| **Data Breaches**       | Facial data could be stolen        | Encrypt database, secure storage, access controls    |
| **Unauthorized Access** | Someone could access the system    | Strong authentication, role-based access, audit logs |
| **Model Tampering**     | Trained model could be manipulated | Model signing, integrity checks, secure storage      |
| **Replay Attacks**      | Old video footage could be used    | Timestamps, session tokens, liveness detection       |

### 9.5 Scalability Challenges

| Challenge                | Description                            | Potential Solutions                                                |
| ------------------------ | -------------------------------------- | ------------------------------------------------------------------ |
| **Large User Base**      | System slow with 1000+ employees       | Distributed processing, cloud deployment, face embeddings indexing |
| **Multiple Locations**   | Need to manage attendance across sites | Centralized database, local caching, microservices                 |
| **Real-Time Processing** | Delay in attendance marking            | Edge computing, parallel processing, optimized algorithms          |
| **Data Backup**          | Loss of facial data is critical        | Regular automated backups, redundant storage, cloud backup         |

---

## 10. ARCHITECTURE PATTERN SUMMARY

This system follows a **Layered Architecture** with clear separation:

- **Presentation Layer**: GUI windows built with PySide6
- **Controller Layer**: Request handlers that coordinate between UI and services
- **Service Layer**: Business logic containing core functionality
- **Data Layer**: Database operations and data models

This architecture provides:

- Loose coupling between components
- Easy maintenance and testing
- Clear separation of concerns
- Scalability for future features
