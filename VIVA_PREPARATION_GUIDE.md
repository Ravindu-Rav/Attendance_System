# VIVA PRESENTATION GUIDE
## Face Recognition Attendance System

---

## 📋 TABLE OF CONTENTS
1. Project Overview
2. Architecture & System Design
3. Technology Stack
4. Key Features Explained
5. Database Schema
6. System Workflow
7. Code Structure Breakdown
8. Key Implementation Details
9. Common Viva Questions & Answers
10. Troubleshooting & Edge Cases

---

## 1️⃣ PROJECT OVERVIEW

### What is the Project?
A **Face Recognition-based Employee Attendance System** that automatically tracks employee check-in and check-out times using facial recognition technology.

### Why Did You Build It?
- **Problem to Solve**: Traditional attendance systems (manual entry, biometric fingerprint) are:
  - Prone to fraud/proxy attendance
  - Time-consuming
  - Not scalable for large organizations
  
- **Solution**: Automated face recognition with:
  - Real-time processing
  - Non-invasive (no physical contact)
  - Modern GUI interface
  - Secure admin controls

### Key Objectives Achieved
1. ✅ Secure login system with role-based access (Admin/Employee)
2. ✅ Employee management with face capture
3. ✅ Real-time face recognition with accuracy control
4. ✅ Attendance tracking with check-in/check-out modes
5. ✅ Early-leave approval workflow
6. ✅ Dashboard with analytics and reporting
7. ✅ CSV export of attendance records

---

## 2️⃣ ARCHITECTURE & SYSTEM DESIGN

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                   │
│            (PySide6 GUI - Main Interface)               │
├─────────────────────────────────────────────────────────┤
│  LoginWindow → DashboardWindow → AttendanceWindow      │
│  AdminPanelWindow → TrainingWindow → EmployeeWindow    │
├─────────────────────────────────────────────────────────┤
│                    CONTROLLER LAYER                      │
│                  (Business Logic Flow)                   │
├─────────────────────────────────────────────────────────┤
│  AuthController → AttendanceController → TrainingCtrl  │
│  RegistrationController                                 │
├─────────────────────────────────────────────────────────┤
│                    SERVICE LAYER                        │
│                  (Core Business Logic)                  │
├─────────────────────────────────────────────────────────┤
│  FaceRecognitionService → TrainingService              │
│  RegistrationService → AttendanceService               │
│  DashboardService → AuthService                        │
├─────────────────────────────────────────────────────────┤
│                    DATA LAYER                           │
│            (Models, Repository, Database)               │
├─────────────────────────────────────────────────────────┤
│  Employee Model → EmployeeRepository                   │
│  Admin Model → AdminRepository                         │
│  SQLite Database (attendance.db)                        │
├─────────────────────────────────────────────────────────┤
│                    EXTERNAL SYSTEMS                      │
│            (OpenCV, Hardware - Camera)                  │
└─────────────────────────────────────────────────────────┘
```

### Design Pattern Used: MVC (Model-View-Controller)
- **Model**: Employee, Admin, Database
- **View**: PySide6 GUI windows
- **Controller**: Business logic routing

### Data Flow Example: Attendance Marking
```
User Face Detected
    ↓
FaceRecognitionService.start_face_recognition()
    ↓
Load LBPH Recognizer Model (trainer.yml)
    ↓
Detect Face using Haar Cascade Classifier
    ↓
Compare with trained model → Get confidence score
    ↓
If confidence > threshold (60):
    ├─ Get Employee ID
    ├─ Check if already marked today
    └─ Insert record in On_Duty table
    ↓
Display Success/Error Message
```

---

## 3️⃣ TECHNOLOGY STACK

### Dependencies & Versions
| Technology | Version | Purpose |
|-----------|---------|---------|
| **OpenCV** | 4.13.0.92 | Face detection & recognition |
| **OpenCV-Contrib** | 4.13.0.92 | LBPH Face Recognizer algorithm |
| **PySide6** | ≥6.7.0 | GUI framework (Qt wrapper) |
| **NumPy** | 2.4.4 | Numerical computing |
| **SQLite3** | Built-in | Relational database |
| **Python** | 3.x | Programming language |

### Why These Technologies?

**OpenCV for Face Recognition**
- Industry standard for computer vision
- LBPH (Local Binary Patterns Histograms) algorithm is lightweight & fast
- No dependency on cloud services
- Works offline

**PySide6 for GUI**
- Modern, cross-platform (Windows/Mac/Linux)
- Native look and feel
- Rich widget library
- Python binding for Qt

**SQLite for Database**
- Lightweight, file-based
- No server setup needed
- Perfect for desktop applications
- ACID compliant

---

## 4️⃣ KEY FEATURES EXPLAINED

### Feature 1: First-Time Admin Registration
**Purpose**: Set up the first admin account when app launches for the first time

**Process**:
```
Login Screen → "Create one" link
    ↓
Opens Admin Registration Window
    ↓
Enter Username & Password
    ↓
Validate & Hash Password
    ↓
Save to Admin table
    ↓
Re-login with credentials
```

**Code Location**: [app/controllers/auth_controller.py](app/controllers/auth_controller.py)

### Feature 2: Employee Management
**Capabilities**:
- Add new employees with details (name, age, gender, email, department)
- Capture 50 face samples per employee from webcam
- Edit employee information
- Delete employees

**Dataset Structure**:
```
dataset/
├── 1/          (Employee ID 1)
│   ├── 1.jpg
│   ├── 2.jpg
│   └── ... (50 samples)
├── 2/
│   ├── 1.jpg
│   └── ...
└── ...
```

### Feature 3: Model Training
**What**: LBPH Face Recognizer training

**How**:
```
Read all images from dataset/ folder
    ↓
Group by Employee ID
    ↓
Convert to grayscale & extract faces
    ↓
Train LBPH Recognizer model
    ↓
Save model as trainer.yml
```

**Configuration**:
- Training Data Split: 80% train, 20% test
- Model Output: `models_storage/trainer.yml`
- Algorithm: LBPH (Local Binary Patterns Histograms)

**Code Location**: [app/services/training_service.py](app/services/training_service.py)

### Feature 4: Real-Time Face Recognition & Attendance
**Workflow**:
1. **Detection**: Haar Cascade classifier detects faces in frame
2. **Recognition**: LBPH model predicts employee ID
3. **Validation**: Confidence score compared to threshold (60)
4. **Recording**: Mark check-in/out time in database
5. **Approval**: Admin approves early leave requests

**Confidence Threshold Logic**:
- Score < 60 → Highly accurate recognition ✅
- Score ≥ 60 → Low confidence, reject ❌

(Lower confidence = better match in LBPH)

### Feature 5: Check-In / Check-Out System
**Rules**:
- Workday: 08:00 - 16:00
- Full day: 8 hours
- Early checkout (< 8 hrs) requires admin approval

**Status Codes**:
- `IN` - Check-in marked
- `OUT` - Check-out marked
- Early leave pending/approved

### Feature 6: Dashboard & Analytics
**Sections**:
1. **Overview Tab**: Total employees, departments, attendance stats
2. **Attendance Tab**: View all records, search, filter
3. **Admin Panel**: Approve/reject early leave requests
4. **CSV Export**: Download attendance records

### Feature 7: Security Features
**Authentication**:
- Admin login with username & password
- Employee login with email & password
- Password hashing (utility in [app/utils/password_utils.py](app/utils/password_utils.py))

**Authorization**:
- Admin-only permissions (edit employees, approve leave)
- Role-based access control

---

## 5️⃣ DATABASE SCHEMA

### Tables Overview

#### 1. **Department Table**
```sql
CREATE TABLE Department (
    dept_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL
);
```
**Purpose**: Store organization departments (HR, IT, Finance, etc.)

---

#### 2. **Employee Table (Core)**
```sql
CREATE TABLE Employee (
    employee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    gender INTEGER,           -- 1=Male, 2=Female
    age INTEGER,
    contact_add TEXT,
    emp_email TEXT UNIQUE,
    emp_pass TEXT,            -- Hashed password
    dept_ID INTEGER,
    FOREIGN KEY(dept_ID) REFERENCES Department(dept_ID)
);
```
**Purpose**: Store employee information
**Relationships**: Links to Department table

---

#### 3. **Admin Table**
```sql
CREATE TABLE Admin (
    admin_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,   -- Hashed
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```
**Purpose**: Store admin credentials

---

#### 4. **Job_Title Table**
```sql
CREATE TABLE Job_Title (
    job_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT NOT NULL,
    dept_ID INTEGER,
    employee_ID INTEGER,
    FOREIGN KEY(dept_ID) REFERENCES Department(dept_ID),
    FOREIGN KEY(employee_ID) REFERENCES Employee(employee_ID)
);
```
**Purpose**: Store job positions and assignments

---

#### 5. **On_Duty Table (Attendance Records)**
```sql
CREATE TABLE On_Duty (
    duty_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_ID INTEGER,
    job_ID INTEGER,
    duration INTEGER,                -- Hours worked
    date TEXT,                        -- YYYY-MM-DD
    in_time TEXT,                     -- HH:MM:SS
    out_time TEXT,                    -- HH:MM:SS (NULL if not checked out)
    status TEXT,                      -- 'IN', 'OUT', 'EARLY_LEAVE'
    early_leave_approved INTEGER DEFAULT 0,  -- 0=pending, 1=approved
    FOREIGN KEY(employee_ID) REFERENCES Employee(employee_ID),
    FOREIGN KEY(job_ID) REFERENCES Job_Title(job_ID)
);
```
**Purpose**: Track attendance records
**Key Relationships**: Links to Employee

---

### Database Relationships Diagram
```
Department (1) ──────── (Many) Employee
                              │
                              │ employee_ID
                              ↓
                         On_Duty (Attendance)
                              │
                              └──→ Stored face in dataset/

Admin (Independent - for system auth)
```

---

## 6️⃣ SYSTEM WORKFLOW

### ⏰ Complete User Journey

#### **ADMIN WORKFLOW**
```
1. Launch App (run.py)
   ├─ Initialize Database (db.py)
   └─ Open Login Window

2. First Time Admin Registration
   ├─ Click "Create one" link
   ├─ Enter username & password
   ├─ Password hashing
   └─ Save to Admin table

3. Admin Login
   ├─ Enter username & password
   ├─ Verify credentials from Admin table
   └─ Open Dashboard (Main Window)

4. Dashboard Operations
   ├─ Overview Tab
   │  ├─ View total employees
   │  ├─ View departments
   │  └─ See attendance statistics
   │
   ├─ Attendance Tab
   │  ├─ View all attendance records
   │  ├─ Search by employee/date
   │  └─ Export to CSV
   │
   └─ Admin Panel Tab
      ├─ View early leave requests
      ├─ Approve/Reject requests
      └─ Update database
```

#### **EMPLOYEE REGISTRATION WORKFLOW**
```
1. Admin → Click "Employee Management"
   ├─ Opens Employee Window

2. Add New Employee
   ├─ Enter: Name, Email, Password, Age, Gender, Department
   ├─ Create record in Employee table
   └─ Return Employee ID

3. Capture Face Samples
   ├─ Webcam opens automatically
   ├─ Detect faces using Haar Cascade
   ├─ Capture 50 samples (configurable)
   ├─ Save as: dataset/{employee_id}/1.jpg ... 50.jpg
   └─ Close webcam → Face samples stored

4. Ready for Training
```

#### **MODEL TRAINING WORKFLOW**
```
1. Admin → Click "Training"
   ├─ Opens Training Window

2. Train Model
   ├─ Click "Train Recognition Model"
   │
   └─ TrainingService.train_model()
      ├─ Load all images from dataset/
      ├─ Group by employee_ID
      ├─ Create face_samples []
      ├─ Create ids []
      │
      ├─ Instantiate cv2.face.LBPHFaceRecognizer_create()
      ├─ recognizer.train(faces, ids)
      ├─ recognizer.save(models_storage/trainer.yml)
      │
      └─ Model ready for recognition

3. Confirmation Message
   └─ "Model training complete!"
```

#### **ATTENDANCE MARKING WORKFLOW**
```
1. Admin/Employee → Click "Check Attendance"
   ├─ Opens Attendance Window

2. Select Mode
   ├─ Check-In → Check current status
   ├─ Check-Out → Mark departure
   └─ Based on today's first record

3. Face Recognition Process
   ├─ Face Recognition Service starts
   ├─ Webcam opens
   │
   ├─ While frame available:
   │  ├─ Capture frame
   │  ├─ Convert to grayscale
   │  ├─ Detect faces (Haar Cascade)
   │  │
   │  └─ For each detected face:
   │     ├─ Load trainer.yml model
   │     ├─ Predict: (employee_id, confidence)
   │     ├─ If confidence < threshold (60):
   │     │  ├─ Get employee name
   │     │  ├─ Check if attendance already marked today
   │     │  ├─ Insert into On_Duty table
   │     │  │  ├─ employee_ID: recognized ID
   │     │  │  ├─ in_time: current time
   │     │  │  ├─ date: today's date
   │     │  │  └─ status: 'IN' or 'OUT'
   │     │  │
   │     │  └─ Show Success: "Marked In/Out"
   │     │
   │     └─ Else:
   │        └─ Show Error: "Low confidence, try again"
   │
   └─ Press ESC → Close webcam

4. Record in Database
   ├─ On_Duty table updated
   ├─ Timestamp recorded
   └─ Ready for next action
```

#### **EARLY LEAVE APPROVAL WORKFLOW**
```
1. Employee checks out early (< 8 hours)
   ├─ System detects early exit
   └─ Sets early_leave_approved = 0 (pending)

2. Record in On_Duty table
   ├─ duration: calculated hours (e.g., 6)
   ├─ status: 'EARLY_LEAVE'
   └─ early_leave_approved: 0

3. Admin Dashboard → Admin Panel
   ├─ View pending early leave requests
   ├─ See employee details & duration
   │
   └─ Options:
      ├─ APPROVE → early_leave_approved = 1
      └─ REJECT → delete or mark as rejected

4. Employee sees record in attendance history
   └─ Status shown with approval indicator
```

---

## 7️⃣ CODE STRUCTURE BREAKDOWN

### Project Directory Layout
```
Attendance_System/
│
├── run.py                          # GUI entry point
├── app/main.py                     # CLI entry point
│
├── app/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py            # Global configuration
│   │
│   ├── controllers/
│   │   ├── auth_controller.py      # Login/Registration logic
│   │   ├── attendance_controller.py # Attendance marking
│   │   ├── registration_controller.py # Employee registration
│   │   └── training_controller.py  # Model training
│   │
│   ├── database/
│   │   └── db.py                  # Database initialization & connection
│   │
│   ├── models/
│   │   ├── employee.py            # Employee model class
│   │   ├── employee_repository.py  # Employee CRUD operations
│   │   ├── admin.py               # Admin model class
│   │   └── admin_repository.py    # Admin CRUD operations
│   │
│   ├── presentation/gui/
│   │   ├── login_window.py         # Login screen
│   │   ├── admin_registration_window.py # Admin registration
│   │   ├── main_window.py          # Dashboard/MainWindow
│   │   ├── employee_window.py      # Employee management
│   │   ├── attendance_window.py    # Attendance marking
│   │   ├── training_window.py      # Model training UI
│   │   └── dashboard_window.py     # Admin dashboard
│   │
│   ├── services/
│   │   ├── face_recognition_service.py  # OpenCV face recognition ⭐
│   │   ├── training_service.py          # Model training logic ⭐
│   │   ├── registration_service.py      # Employee registration ⭐
│   │   ├── attendance_service.py        # Attendance logic
│   │   ├── dashboard_service.py         # Analytics & reporting
│   │   └── auth_service.py              # Authentication
│   │
│   └── utils/
│       └── password_utils.py       # Password hashing/validation
│
├── dataset/                        # Face image database
│   ├── 1/
│   │   ├── 1.jpg
│   │   ├── 2.jpg
│   │   └── ... (50 samples per employee)
│   ├── 2/
│   │   └── ...
│   └── ...
│
├── models_storage/
│   └── trainer.yml                # Trained LBPH model
│
├── attendance.db                  # SQLite database
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

### Key Files & Their Responsibilities

| File | Responsibility | Lines of Code |
|------|-----------------|---------------|
| `run.py` | GUI entry point, DB init | ~20 |
| `app/config/settings.py` | Configuration constants | ~40 |
| `app/database/db.py` | Database init, schema creation | ~70 |
| `app/services/face_recognition_service.py` | Real-time face recognition, attendance marking | ~80 |
| `app/services/training_service.py` | LBPH model training from dataset | ~60 |
| `app/services/registration_service.py` | Employee registration, face capture | ~90 |
| `app/models/employee_repository.py` | Employee CRUD operations | ~50 |
| `app/models/admin_repository.py` | Admin CRUD operations | ~50 |
| `app/controllers/attendance_controller.py` | Attendance controller | ~15 |
| `app/presentation/gui/login_window.py` | Login UI | ~100+ |
| `app/presentation/gui/dashboard_window.py` | Main dashboard UI | ~150+ |

---

## 8️⃣ KEY IMPLEMENTATION DETAILS

### LBPH Face Recognizer Algorithm
**What is LBPH?**
- Local Binary Patterns Histograms
- Lightweight, uses local texture information
- Compares patterns around each pixel

**Why LBPH?**
1. ✅ Fast - works in real-time
2. ✅ Lightweight - runs on any machine
3. ✅ No cloud dependency - fully offline
4. ✅ Good accuracy for controlled environments

**How It Works**:
```
Training Phase:
├─ Load all employee face images
├─ For each image:
│  ├─ Divide into regions
│  ├─ Extract LBP pattern for each region
│  └─ Create histogram
├─ Store histograms + labels
└─ Save model

Recognition Phase:
├─ Capture unknown face
├─ Extract same LBP patterns
├─ Compare with stored histograms
├─ Return closest match (employee_id, confidence)
└─ If confidence < 60 → Recognize
```

### Haar Cascade Classifier
**Purpose**: Detect faces in real-time video frames

**Why?**: 
- Fast, cascade-based detection
- Pre-trained classifier available in OpenCV
- Works well for frontal faces

**File**: `haarcascade_frontalface_default.xml` (built-in with OpenCV)

### Face Capture Logic
```python
# Key code from registration_service.py

def capture_faces(employee_id, num_samples=50):
    # 1. Create dataset folder: dataset/{employee_id}/
    # 2. Initialize cascade classifier
    # 3. Open webcam
    # 4. Loop until num_samples captured:
    #    ├─ Read frame
    #    ├─ Convert to grayscale (faster processing)
    #    ├─ Detect faces
    #    ├─ For each face:
    #    │  ├─ Extract region
    #    │  ├─ Save as {employee_id}/{count}.jpg
    #    │  └─ Draw rectangle + counter
    #    └─ Display frame
    # 5. ESC to exit, release camera
```

### Attendance Marking Logic
```python
# Key code from face_recognition_service.py

def mark_attendance(employee_id):
    # 1. Check if already marked today
    # 2. If not marked:
    #    ├─ Get current date & time
    #    ├─ Determine IN/OUT based on previous record
    #    ├─ Insert into On_Duty table
    #    └─ Return success
    # 3. If already marked:
    #    └─ Return failure (already marked)
```

### Password Security
```python
# app/utils/password_utils.py

# Passwords are hashed (not stored in plain text)
# Uses Python's built-in hashing mechanisms
# Password min length: 6 characters
```

### Configuration Management
**All settings in one place**: `app/config/settings.py`

```python
# Face Recognition
FACE_RECOGNITION_CONFIDENCE_THRESHOLD = 60    # Lower = better
DEFAULT_CAPTURE_SAMPLES = 50                  # Samples per employee

# Camera
CAMERA_INDEX = 0                              # Primary camera
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Database
DATABASE_NAME = "attendance.db"

# Model
MODEL_PATH = "models_storage/trainer.yml"
```

---

## 9️⃣ COMMON VIVA QUESTIONS & ANSWERS

### Q1: "What problem does your project solve?"
**Answer:**
> Employee attendance management in traditional systems is manual, time-consuming, and prone to fraud (proxy attendance). Our system automates this using face recognition technology, ensuring real-time, accurate, and tamper-proof attendance tracking. This is especially useful for large organizations with many employees.

---

### Q2: "Why did you choose LBPH over other face recognition algorithms?"
**Answer:**
> LBPH (Local Binary Patterns Histograms) was chosen because:
> 1. **Lightweight & Fast**: Runs in real-time without GPU
> 2. **Offline**: No cloud dependency or API calls
> 3. **Good Accuracy**: Sufficient for controlled environments (office)
> 4. **Easy Implementation**: Built-in OpenCV, minimal training required
> 
> Other alternatives (like Deep Learning models - VGGFace, FaceNet) require:
> - GPU/significant compute
> - Large training datasets
> - Pre-trained weights
> - Slow inference on CPU

---

### Q3: "How does your system ensure security?"
**Answer:**
> Security measures include:
> 1. **Authentication**: Admin login with username/password (required before any action)
> 2. **Password Hashing**: Passwords stored hashed, not plain text
> 3. **Role-Based Access**: Admin-only features (approve leave, manage employees)
> 4. **Face Recognition Threshold**: Confidence scores prevent imposters
> 5. **Approval Workflow**: Early leave requires admin sign-off
> 6. **Database Transactions**: ACID compliance prevents data corruption

---

### Q4: "How do you handle false positives in face recognition?"
**Answer:**
> Several strategies implemented:
> 1. **Confidence Threshold (60)**: Only accepts high-confidence matches
> 2. **Multiple face samples (50)**: Training with diverse angles/lighting improves accuracy
> 3. **Daily One-Entry Rule**: Can't mark attendance twice same day
> 4. **Admin Override**: Admins can manually edit records if needed
> 5. **Re-training**: If accuracy degrades, retrain model with new samples

---

### Q5: "What technologies are used and why?"
**Answer:**
> | Component | Tech | Why |
> |-----------|------|-----|
> | GUI | PySide6 | Modern, cross-platform, native look |
> | Computer Vision | OpenCV | Industry standard, lightweight |
> | Database | SQLite | File-based, no server, suitable for desktop |
> | Backend Logic | Python | Easy to learn, rapid development, rich libraries |
> | Algorithms | LBPH | Fast, lightweight, good accuracy |

---

### Q6: "How does the face capture and training process work?"
**Answer:**
> **Face Capture Process**:
> 1. Admin registers employee and initiates face capture
> 2. Webcam opens, Haar Cascade detector finds faces
> 3. System captures 50 samples from different angles/distances
> 4. Images saved as `dataset/{employee_id}/{sample_number}.jpg`
> 5. ESC or reach 50 samples → process ends
>
> **Training Process**:
> 1. Read all images from dataset/
> 2. Convert to grayscale (speed optimization)
> 3. Create LBPH recognizer object
> 4. Train with all faces and corresponding employee IDs
> 5. Save model to `models_storage/trainer.yml`
> 6. Model ready for real-time recognition

---

### Q7: "What happens if an employee checks in early or leaves early?"
**Answer:**
> **Early Leave Workflow**:
> 1. Employee checks out before 16:00 (workday end)
> 2. System calculates duration worked (< 8 hours)
> 3. Record saved with `status='EARLY_LEAVE'` and `early_leave_approved=0` (pending)
> 4. Admin sees pending request in Dashboard → Admin Panel
> 5. Admin can APPROVE or REJECT
> 6. If approved: `early_leave_approved=1`, employee's leave is validated
> 7. If rejected: record marked as unapproved
> 8. Employee can see history in attendance tab

---

### Q8: "How is the database structured?"
**Answer:**
> **Key Tables**:
> - **Employee**: Stores employee details (name, email, password, department)
> - **Admin**: Stores admin credentials (username, password)
> - **Department**: Lists departments
> - **Job_Title**: Employee job positions
> - **On_Duty**: Attendance records (check-in, check-out, times, duration)
>
> **Relationships**:
> - Employee ← Foreign Key → Department
> - On_Duty ← Foreign Key → Employee
> - One employee can have many attendance records
> - All data persists to `attendance.db` (SQLite file)

---

### Q9: "How does the system know whether to record Check-In or Check-Out?"
**Answer:**
> **Logic**:
> 1. When attendance is clicked, system checks if employee has record for today
> 2. **If no record today**: Mark as CHECK-IN (first entry of day)
> 3. **If record exists but no out_time**: Mark as CHECK-OUT (update existing record)
> 4. **If both in_time and out_time exist**: Show error (already marked in & out)
>
> This is done by querying the On_Duty table:
> ```sql
> SELECT * FROM On_Duty 
> WHERE employee_ID=? AND date=TODAY
> ```
> If result is NULL → CHECK-IN, else → CHECK-OUT

---

### Q10: "What are potential scalability issues?"
**Answer:**
> **Current Limitations**:
> 1. **SQLite**: Single user access, not suitable for 100+ concurrent users
>    - *Solution*: Migrate to PostgreSQL/MySQL for multi-user scenarios
> 2. **LBPH Accuracy**: Degrades with large face databases (500+ employees)
>    - *Solution*: Switch to deep learning models (VGGFace, FaceNet)
> 3. **Face Recognition Speed**: Slower with each new model retraining
>    - *Solution*: Implement incremental learning or use pre-trained models
> 4. **Single Webcam**: One camera per workstation
>    - *Solution*: Deploy multiple cameras with network connectivity
> 5. **Manual Face Capture**: 50 samples per employee takes time
>    - *Solution*: Use automated sampling over multiple days

---

### Q11: "How would you handle system failures?"
**Answer:**
> **Failure Scenarios & Solutions**:
> 
> | Failure | Cause | Solution |
> |---------|-------|----------|
> | Model not found | Training not done | Guide user to train model first |
> | Camera not detected | Webcam disconnected/in use | Show error, allow retry |
> | Database locked | Multiple instances running | Single instance enforcement |
> | Low face accuracy | Poor samples/training data | Re-capture samples, retrain |
> | Attendance already marked | Person tried to mark twice | Check database before insert |

---

### Q12: "Can you explain the MVC architecture you used?"
**Answer:**
> **Model-View-Controller Pattern**:
> 
> **Model** (Data Layer):
> - Employee.py, Admin.py classes
> - EmployeeRepository, AdminRepository (CRUD)
> - Database schema in db.py
> - Owns business rules
>
> **View** (Presentation Layer):
> - PySide6 GUI windows (login_window, dashboard_window, etc.)
> - Displays data to user
> - Captures user input
> - No business logic
>
> **Controller** (Logic Layer):
> - auth_controller, attendance_controller, etc.
> - Receives user input from View
> - Processes using Services
> - Updates Model & View
>
> **Flow**:
> ```
> User Input (View) → Controller → Service/Model → Database
> Database → Model → Service → Controller → Update View
> ```

---

### Q13: "How do you ensure data integrity?"
**Answer:**
> **Data Integrity Mechanisms**:
> 1. **Primary Keys**: Each table has unique ID
> 2. **Foreign Keys**: Enforce relationships (Employee → Department)
> 3. **Unique Constraints**: Email is unique in Employee table
> 4. **NOT NULL Constraints**: Required fields can't be empty
> 5. **DEFAULT Values**: Auto-fill defaults (timestamp, approval status)
> 6. **Transactions**: ACID compliance ensures consistent state
> 7. **Validation**: Check before insertion (e.g., confidence threshold)

---

### Q14: "What is the confidence threshold and how is it used?"
**Answer:**
> **Confidence Threshold = 60**
>
> - This is a **distance metric** from LBPH algorithm
> - **Lower score = Better match** (more similar to training images)
> - **Logic**:
>   - If confidence **< 60** → Recognize (high accuracy) ✅
>   - If confidence **≥ 60** → Reject (uncertain) ❌
>
> **Why 60?**
> - Empirically determined through testing
> - Balances false positives vs false negatives
> - Can be adjusted in `settings.py` if needed
>
> **Example**:
> - Employee ID 5: confidence = 45 → ACCEPT (likely genuine)
> - Unknown person: confidence = 95 → REJECT (clearly doesn't match)

---

### Q15: "How would you test this system?"
**Answer:**
> **Testing Strategies**:
> 
> **1. Unit Testing**:
> - Test individual functions (password validation, date parsing)
> - Mock database calls
> 
> **2. Integration Testing**:
> - Test controller → service → model flow
> - Verify database operations
>
> **3. Face Recognition Testing**:
> - Use diverse test faces (different lighting, angles)
> - Measure accuracy (True Positive Rate, False Positive Rate)
> - Test with distorted/mask faces
>
> **4. GUI Testing**:
> - Test all windows open correctly
> - Verify button clicks trigger correct actions
> - Check error messages display properly
>
> **5. Database Testing**:
> - Verify schema creation
> - Test constraints (unique email, foreign keys)
> - Verify transaction rollback on errors
>
> **6. Stress Testing**:
> - Mark attendance for 100+ employees
> - Train model with 1000+ images
> - Check performance degradation

---

## 🔟 TROUBLESHOOTING & EDGE CASES

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| **"Model not trained"** | trainer.yml missing | Go to Training window → Train model |
| **Camera not opening** | Webcam already in use | Close other apps, check permissions |
| **Low attendance accuracy** | Poor face quality initial capture | Re-capture 50 samples in good lighting |
| **Database locked** | Multiple app instances | Close all instances, restart |
| **"No face detected"** | Face not in frame | Move closer, ensure good lighting |
| **Employee appears twice in table** | Duplicate entry | Check unique constraints, purge duplicates |
| **Can't mark attendance** | Face quality poor | Retrain model with better samples |

### Edge Cases Handled

1. **Same person, different roles?**
   - Not supported - one face → one employee ID
   - Could be solved by multi-person recognition

2. **Twins/similar-looking employees?**
   - LBPH may confuse them
   - Solution: Manual verification, role-based confirmation

3. **Employee with facial hair/glasses changes?**
   - Model retraining recommended if styles change significantly
   - Current system relies on consistency

4. **Night shift employees?**
   - System handles any time - no time-based restrictions in code

5. **Seasonal/temporary employees?**
   - Delete employee → face dataset removed
   - Re-add when they return

6. **Power outage during training?**
   - Model file incomplete
   - Re-trigger training

---

## 📚 GLOSSARY

| Term | Definition |
|------|-----------|
| **LBPH** | Local Binary Patterns Histograms - face recognition algorithm |
| **Confidence Score** | Distance metric from LBPH; lower = better match |
| **Haar Cascade** | Pre-trained classifier for face detection |
| **Grayscale** | Single-channel image format (faster than RGB) |
| **ROI** | Region of Interest - detected face area |
| **Prime Key** | Unique identifier for each record |
| **Foreign Key** | Reference to another table's primary key |
| **Threshold** | Cutoff value for decision making |
| **Epoch** | One complete pass through training data |
| **True Positive** | Correct recognition of known person |
| **False Positive** | Incorrect recognition (wrong person accepted) |
| **False Negative** | Correct rejection of known person |
| **Dataset** | Collection of training face images |
| **Model** | Trained recognizer (trainer.yml) |
| **Session** | User login instance |
| **Repository Pattern** | Data access layer abstraction |
| **MVC** | Model-View-Controller architecture |

---

## 🎓 FINAL TIPS FOR VIVA

✅ **DO**:
- Understand each component deeply
- Explain "Why" behind decisions (LBPH vs alternatives)
- Show confidence in knowledge
- Admit limitations honestly (scalability, accuracy)
- Provide real examples/scenarios
- Ask clarifying questions if needed

❌ **DON'T**:
- Memorize code line-by-line
- Overcomplicate simple concepts
- Make up features that don't exist
- Ignore edge cases
- Claim perfect 100% accuracy
- Pretend to know something you don't

### Must-Know Points:
1. **Architecture**: MVC, layered design
2. **Algorithm**: LBPH, why chosen, how it works
3. **Workflow**: Complete user journey (registration → training → attendance)
4. **Database**: Table relationships, schema design
5. **Security**: Authentication, role-based access
6. **Validation**: Confidence threshold, daily check limits
7. **Error Handling**: What happens when things fail

### Potential Deep-Dive Questions:
- "Show me the face recognition code"
- "How would you improve accuracy to 99%?"
- "Design for 10,000 employees - what changes?"
- "Explain the exact process from face detection to database insertion"
- "What's the time complexity of your main algorithms?"

---

**Good luck with your viva! 🚀**
