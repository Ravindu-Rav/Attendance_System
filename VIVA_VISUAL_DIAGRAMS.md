# VISUAL DIAGRAMS & FLOWCHARTS FOR VIVA
## Face Recognition Attendance System

---

## 📊 SYSTEM ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                        │
│  (PySide6 GUI - Handles all visual interaction)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LoginWindow      MainWindow       EmployeeWindow              │
│       │               │                   │                     │
│       │          DashboardWindow     TrainingWindow            │
│       │               │                   │                     │
│       └───────────────┼───────────────────┘                     │
│                       │                                         │
│            AttendanceWindow (Scanner)                          │
│                       │                                         │
└───────────────────────┼─────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────────┐
│               CONTROLLER LAYER (Routing)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AuthController → RegistrationController                       │
│       │                   │                                     │
│  AttendanceController → TrainingController                     │
│       │                   │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER (Core Logic)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ⭐ FaceRecognitionService (CRITICAL)                          │
│      - start_face_recognition()                                │
│      - mark_attendance()                                        │
│      - identify_employee()                                      │
│                                                                 │
│  ⭐ TrainingService (CRITICAL)                                 │
│      - train_model()                                            │
│      - get_images_and_labels()                                 │
│                                                                 │
│  ⭐ RegistrationService (CRITICAL)                             │
│      - capture_faces()                                          │
│      - add_employee()                                           │
│                                                                 │
│  AttendanceService, DashboardService, AuthService              │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                     MODEL & DATA LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Employee.py → EmployeeRepository → SQLite                    │
│  Admin.py → AdminRepository → SQLite                          │
│                                                                 │
│  Database Tables:                                              │
│  ├─ Employee (ID, name, email, dept)                          │
│  ├─ Admin (username, password)                                │
│  ├─ Department (dept name)                                    │
│  ├─ Job_Title (job assignment)                               │
│  └─ On_Duty ⭐ (check-in/out, timestamps)                    │
│                                                                 │
│  attendance.db (SQLite file)                                   │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│              EXTERNAL SYSTEMS & STORAGE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📷 Webcam (Camera input)                                       │
│      ↓                                                          │
│  🔍 OpenCV (Face detection + recognition)                     │
│      ├─ Haar Cascade (Face detection)                         │
│      └─ LBPH Algorithm (Face recognition)                     │
│                                                                 │
│  📦 File System Storage                                        │
│      ├─ dataset/ (50 samples per employee)                    │
│      ├─ models_storage/trainer.yml (trained model)           │
│      └─ attendance.db (SQLite database)                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 COMPLETE WORKFLOW (End-to-End)

```
SCENARIO: First Day Setup → Employee Attendance

ADMIN WORKFLOW
══════════════════════════════════════════════════════════════════

Day 1 - Setup:
┌──────────────┐
│  Launch App  │
└──────┬───────┘
       ↓
┌──────────────────────────────┐
│  Database Initialization     │
│  (db.py → init_db())         │
│  Creates:                    │
│  - Employee table            │
│  - Admin table               │
│  - On_Duty table             │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Admin Registration Window   │
│  (First time only)           │
│  Enter: username, password   │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Admin Repository            │
│  Hash password (security)    │
│  Save to Admin table         │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Login Window                │
│  (Next launches)             │
│  Verify credentials          │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Dashboard/Main Window       │
│  Admin is now logged in ✅   │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Employee Management Window  │
│  - Add New Employee          │
│  - Enter: name, email, etc   │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Database Insert             │
│  INSERT INTO Employee        │
│  Returns employee_ID = 5     │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Face Capture Phase          │
│  registration_service.py     │
│  Create folder: dataset/5/   │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Webcam Opens                │
│  (cv2.VideoCapture(0))       │
│  Haar Cascade detector loads │
└──────┬───────────────────────┘
       ↓
  [LOOP - Capture 50 samples]
  ┌─────────────────────────┐
  │ Read frame from camera  │
  │ Detect face             │
  │ Save: dataset/5/X.jpg   │
  │ Progress counter        │
  │ Repeat 50 times         │
  └─────────────┬───────────┘
                ↓ (ESC or 50 done)
  ┌─────────────────────────┐
  │ Close webcam            │
  │ Dataset ready ✅        │
  └─────────────┬───────────┘
                ↓
┌──────────────────────────────┐
│  Training Window             │
│  Click "Train Model"         │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  TrainingService.train_model()
│  1. Load dataset/5/*.jpg     │
│  2. Convert to grayscale     │
│  3. Create face array        │
│  4. Create ID array [5,5,...]│
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  LBPH Training               │
│  recognizer.train(faces, ids)│
│  Extract feature patterns    │
│  Build histograms per region │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Save Model                  │
│  recognizer.save(trainer.yml)│
│  models_storage/trainer.yml  │
│  Training Complete! ✅       │
└──────┬───────────────────────┘
       ↓


EMPLOYEE ATTENDANCE FLOW
══════════════════════════════════════════════════════════════════

Day 2 - Mark Attendance:

┌──────────────────────────────┐
│  Employee Clicks Check-In    │
│  (attendance_window.py)      │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  FaceRecognitionService Starts
│  Webcam opens                │
│  Haar Cascade loaded         │
└──────┬───────────────────────┘
       ↓
  [LIVE LOOP - Until Face Recognized]
  ┌──────────────────────────────┐
  │ 1. Capture frame             │
  │ 2. Convert BGR → Grayscale   │
  │ 3. Detect faces              │
  │    (Haar Cascade)            │
  │ 4. Extract face region       │
  └──────┬───────────────────────┘
         ↓
  ┌──────────────────────────────┐
  │ 5. Load trainer.yml model    │
  │ 6. Predict:                  │
  │    (employee_id, conf) =     │
  │    recognizer.predict(face)  │
  │ 7. Check confidence < 60:    │
  │    - YES → Proceed ✅        │
  │    - NO → Show error ❌      │
  └──────┬───────────────────────┘
         ↓
┌──────────────────────────────┐
│  Get Employee Details        │
│  SELECT fname, lname         │
│  FROM Employee               │
│  WHERE employee_ID = 5       │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Check if Already Marked     │
│  SELECT * FROM On_Duty       │
│  WHERE employee_ID=5         │
│  AND date=TODAY              │
│  - Found → Show "Already IN" │
│  - Not found → Continue →    │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Insert Check-In Record      │
│  INSERT INTO On_Duty:        │
│  - employee_ID: 5            │
│  - date: 2024-04-02          │
│  - in_time: 08:15:30         │
│  - status: 'IN'              │
│  - early_leave_approved: 0   │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Close Webcam                │
│  Display SUCCESS             │
│  "Marked IN at 08:15"        │
│  Record in DB ✅             │
└──────────────────────────────┘

[LATER IN DAY - CHECK-OUT]
       ↓
┌──────────────────────────────┐
│  Employee Clicks Check-Out   │
└──────┬───────────────────────┘
       ↓
  [Same process: Detect → Recognize]
       ↓
┌──────────────────────────────┐
│  Check if Already Marked     │
│  SELECT * FROM On_Duty       │
│  WHERE employee_ID=5         │
│  AND date=TODAY              │
│  - Has in_time but NO out_time│
│    → Mark as OUT             │
│  - Has both → Already marked │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  UPDATE On_Duty Record:      │
│  SET out_time: 16:45:15      │
│  SET status: 'OUT'           │
│  Calculate duration:         │
│  16:45 - 08:15 = 8h 30m ✅  │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Check Duration              │
│  IF < 8 hours:               │
│  ├─ Set status='EARLY_LEAVE' │
│  └─ Mark early_leave_approv=0│
│  ELSE: Leave as 'OUT'        │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Display Result              │
│  "Checked OUT at 16:45"      │
│  Record Updated in DB ✅     │
└──────────────────────────────┘

[IF EARLY LEAVE]
       ↓
┌──────────────────────────────┐
│  Admin Dashboard             │
│  → Admin Panel Tab           │
│  Sees pending request:       │
│  Employee 5 - 6 hours worked │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  Admin Decision              │
│  APPROVE or REJECT           │
└──────┬───────────────────────┘
       ↓
┌──────────────────────────────┐
│  UPDATE On_Duty:             │
│  SET early_leave_approved=1  │
│  Record shows: Approved ✅   │
└──────────────────────────────┘
```

---

## 🎯 FACE RECOGNITION ALGORITHM FLOW

```
                        ┌─────────────────────┐
                        │ TRAINING PHASE      │
                        └────────────┬────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                                                         │
        ↓                                                         ↓
    ┌──────────────────┐                          ┌──────────────────────┐
    │ Load Dataset     │                          │ For Each Image:      │
    │ dataset/         │                          ├──────────────────────┤
    │ ├─ 1/            │                          │ • Convert to Gray    │
    │ ├─ 2/            │                          │ • Divide into cells  │
    │ └─ N/            │                          │ • Extract LBP values │
    │                  │                          │ • Create histogram   │
    └────────┬─────────┘                          └─────────┬──────────┘
             │                                              │
             └──────────────────┬───────────────────────────┘
                                │
                                ↓
                    ┌───────────────────────┐
                    │ LBPH Recognizer       │
                    │ Create feature space  │
                    │ Store all histograms  │
                    │ With corresponding IDs│
                    └───────────┬───────────┘
                                │
                                ↓
                    ┌───────────────────────┐
                    │ Save Model            │
                    │ trainer.yml           │
                    │ Ready for use! ✅     │
                    └───────────────────────┘


                    ┌─────────────────────┐
                    │ RECOGNITION PHASE   │
                    └────────────┬────────┘
                                 │
                    ┌────────────────────────┐
                    │ Capture Unknown Face  │
                    │ (From webcam)         │
                    └────────────┬───────────┘
                                 │
                    ┌────────────────────────┐
                    │ Extract Same Features │
                    │ • Convert to Gray     │
                    │ • Extract LBP patterns│
                    │ • Create histogram    │
                    └────────────┬───────────┘
                                 │
                    ┌────────────────────────┐
                    │ Load Saved Model      │
                    │ trainer.yml           │
                    └────────────┬───────────┘
                                 │
                    ┌────────────────────────┐
                    │ Compare with All      │
                    │ Stored Histograms     │
                    │ Find closest match    │
                    └────────────┬───────────┘
                                 │
                    ┌────────────────────────┐
                    │ Return Result         │
                    │ (best_label,          │
                    │  confidence_score)    │
                    └────────────┬───────────┘
                                 │
                    ┌────────────────────────┐
                    │ Decision:             │
                    │ Confidence < 60?      │
                    │ YES → ACCEPT ✅       │
                    │ NO  → REJECT ❌       │
                    └────────────────────────┘
```

---

## 📋 DATABASE RELATIONSHIPS

```
                    ADMIN (System Authorization)
                    ┌──────────────────────────┐
                    │ admin_ID (PK)            │
                    │ username (UNIQUE)        │
                    │ password (HASHED)        │
                    │ created_at               │
                    └──────────────────────────┘
                           (Separate)


        ┌──────────────────────────────────────────┐
        │ DEPARTMENT                               │
        │ ┌────────────────────────────────────┐   │
        │ │ dept_ID (PK)                       │   │
        │ │ department_name                    │   │
        │ └────────┬─────────────────────────────┘   │
        │          │ (1) ◄──── (Many)                │
        │          │                                 │
        └──────────┼─────────────────────────────────┘
                   │
                   │ Foreign Key
                   ↓
        ┌──────────────────────────────────────────┐
        │ EMPLOYEE ⭐ (CORE)                      │
        │ ┌────────────────────────────────────┐   │
        │ │ employee_ID (PK)                   │   │
        │ │ fname, lname                       │   │
        │ │ email (UNIQUE)                     │   │
        │ │ gender, age                        │   │
        │ │ contact_add                        │   │
        │ │ emp_pass (HASHED)                  │   │
        │ │ dept_ID (FK) ───────>┐             │   │
        │ └────┬──────────────────┼─────────────┘   │
        │      │                  │                  │
        │      │ (1) ◄──── (Many) │                  │
        │      │                  └─────────────────┘
        │      │
        │      ├──────────┐
        │      │           │
        │      ↓           ↓
        │   ┌──────────┐  ┌──────────┐
        │   │ JOB_     │  │ ON_DUTY  │
        │   │ TITLE    │  │ ⭐⭐     │
        │   │          │  │          │
        │   └──────────┘  │ duty_ID  │
        │                 │ employee │
        │                 │ _ID(FK)  │
        │                 │ date     │
        │                 │ in_time  │
        │                 │ out_time │
        │                 │ status   │
        │                 │ early_   │
        │                 │ leave_   │
        │                 │ approved │
        │                 └──────────┘
        │
        └──────────────────────────────────────────┘


CRITICAL RELATIONSHIP FOR ATTENDANCE:
┌─────────────────┐        ┌──────────────────┐
│ EMPLOYEE        │ 1 ──→ N│ ON_DUTY          │
│                 │        │                  │
│ employee_ID     │───────→│ employee_ID      │
│ fname, lname    │(FK)    │ date (pk2)       │
│ email           │        │ in_time          │
│ emp_pass        │        │ out_time         │
│                 │        │ duration         │
│                 │        │ status           │
│                 │        │ early_leave_appr │
└─────────────────┘        └──────────────────┘

Each Employee can have MANY attendance records!
```

---

## 🔐 AUTHENTICATION & AUTHORIZATION FLOW

```
┌──────────────────────────────────────┐
│  USER LAUNCHES APP                   │
│  run.py → LoginWindow               │
└──────────────┬───────────────────────┘
               │
       ┌───────▼──────────┐
       │ First Time?      │
       └───┬──────────┬───┘
           │          │
        YES│          │ NO
           ↓          ↓
    ┌────────────┐  ┌──────────────────┐
    │Create Admin│  │Login Window      │
    │Registration│  │ - Username field │
    │ Window     │  │ - Password field │
    │ (Register) │  │ - Login button   │
    └─────┬──────┘  └────────┬─────────┘
          │                  │
          │                  ↓
          │         ┌────────────────┐
          │         │Query Admin     │
          │         │table WHERE     │
          │         │username=?      │
          │         └────────┬───────┘
          │                  │
          │                  ↓
          │         ┌────────────────┐
          │         │ Credentials    │
          │         │ Valid?         │
          │         └───┬────────┬───┘
          │             │        │
          │          YES│        │ NO
          │             ↓        ↓
          │         SUCCESS    ERROR
          │             ↓        │
          │         ┌───┴──────┐ │
          └────────►│ MAIN     │◄┘
                    │ WINDOW   │
                    │ Dashboard│
                    │(AUTHENTICATED)
                    └──────┬───┘
                           │
               ┌───────────┴───────────┐
               │                       │
               ↓                       ↓
    ┌──────────────────┐  ┌──────────────────┐
    │ ADMIN FEATURES   │  │ EMPLOYEE OPTIONS │
    │ ✅ Add employees │  │ ✅ Check-In      │
    │ ✅ Edit employee │  │ ✅ Check-Out     │
    │ ✅ Train model   │  │ ❌ Add employees │
    │ ✅ Approve leave │  │ ❌ Train model   │
    │ ✅ View all data │  │ ✅ See own records
    └──────────────────┘  └──────────────────┘
    (Role-Based Access Control in action!)
```

---

## 📊 CONFIDENCE SCORE VISUALIZATION

```
LBPH Distance Metric (Lower = Better Match):

Confidence Score Range:
0 ─────────────────────────────────────────────── 100+
│
│ EXCELLENT MATCH              POOR MATCH
│ (Definitely this person)    (Probably not)
│
0 - 20:    🎯 Perfect match (almost always genuine)
20 - 40:   🟢 Very good match (high confidence)
40 - 60:   🟡 Good match (acceptable)
60 - 80:   🔴 Uncertain (might be wrong)
80+:       ❌ Almost certainly different person

OUR THRESHOLD = 60 (Conservative approach)
│
├─ Score < 60 → ACCEPT ✅ (Safe to mark attendance)
│
└─ Score ≥ 60 → REJECT ❌ (Too uncertain, try again)


EXAMPLE SCENARIOS:

Employee ID 5 attempts check-in:
├─ Confidence = 35 → ACCEPT ✅ (Very likely genuine)
├─ Confidence = 55 → ACCEPT ✅ (Good enough)
├─ Confidence = 65 → REJECT ❌ (Too uncertain)
└─ Confidence = 95 → REJECT ❌ (Clearly doesn't match)

Unknown person attempts fraud:
└─ Confidence = 90+ → REJECT ❌ (If it matches anyone, 
                      not confident enough)

Note: Different faces might have confidence 
      scores depending on similarity
```

---

## 🧠 LBPH ALGORITHM VISUAL EXPLANATION

```
WHAT IS A LOCAL BINARY PATTERN (LBP)?

Original Pixel & Neighbors (3x3 region):
┌─────┬─────┬─────┐
│  90 │ 100 │  95 │
├─────┼─────┼─────┤
│  85 │ 100 │ 110 │  (center pixel = 100)
├─────┼─────┼─────┤
│  80 │  95 │ 105 │
└─────┴─────┴─────┘

Compare Each Neighbor to Center (100):
┌────┬────┬────┐
│ <  │ =  │ <  │   If neighbor ≥ center: 1
├────┼────┼────┤   If neighbor < center: 0
│ <  │ C  │ >  │
├────┼────┼────┤
│ <  │ <  │ >  │
└────┴────┴────┘

Binary Pattern (reading clockwise from top-left):
┌─────────────────┐
│  0 1 0          │
│  0 1 1  = 01100110 (binary)
│  0 1 1          │  = 102 (decimal)
└─────────────────┘

THIS IS THE "Local Binary Pattern" number!


FOR ENTIRE IMAGE:

1. Divide image into regions (e.g., 8x8 grid)
2. For each region, calculate LBP of all pixels
3. Create histogram of LBP values for that region
4. Do this for all regions
5. CONCATENATE all histograms
6. Result: Feature vector for this face!

LBPH = Local Binary Pattern (per pixel)
       + Histogram (statistics per region)
       + Comparison (matching histograms)
```

---

## ⚠️ ERROR HANDLING FLOWCHART

```
┌────────────────────────────┐
│ Operation Initiated        │
└────────────┬───────────────┘
             │
    ┌────────▼─────────┐
    │ Is Model Trained?│
    └────┬──────────┬──┘
         │          │
        NO          YES
         │          │
         ↓          │
    ┌────────────┐  │
    │"Model not  │  │
    │trained"    │  │
    │ERROR ❌    │  │
    └────────────┘  │
                    ↓
            ┌───────────────────┐
            │ Load trainer.yml  │
            └────┬──────────┬───┘
                 │          │
            SUCCESS         FAIL
                 │          │
                 ↓          ↓
              OK      ┌────────────┐
                      │"File not   │
                      │found error"│
                      │ERROR ❌    │
                      └────────────┘

┌───────────────────────────┐
│ Webcam Not Detected       │
│ (camera not connected)    │
└───┬───────────────────────┘
    │
    ↓
┌──────────────────────┐
│ Can't open camera    │
│ ERROR ❌             │
│ Solution: Check USB, │
│ restart app          │
└──────────────────────┘

┌───────────────────────────┐
│ No Face Detected          │
│ in frame                  │
└───┬───────────────────────┘
    │
    ↓
┌──────────────────────┐
│ Show: "Move closer"  │
│ or "Better lighting" │
│ Keep trying...       │
└──────────────────────┘

┌───────────────────────────┐
│ Face Detected but         │
│ Low Confidence (>= 60)    │
└───┬───────────────────────┘
    │
    ↓
┌──────────────────────┐
│"Unrecognized face"   │
│ ERROR ❌             │
│ Try: Move in frame,  │
│ better angle         │
└──────────────────────┘

┌───────────────────────────┐
│ Already Marked Today      │
│ for this employee         │
└───┬───────────────────────┘
    │
    ↓
┌──────────────────────┐
│ "Attendance already  │
│ marked"              │
│ Show existing record │
└──────────────────────┘

┌───────────────────────────┐
│ Database Insert Failed    │
│ (SQL error)               │
└───┬───────────────────────┘
    │
    ↓
┌──────────────────────┐
│ "DB error"           │
│ Try: Restart app,    │
│ check DB file        │
└──────────────────────┘
```

---

## 💾 FILE ORGANIZATION

```
Attendance_System/
│
├─── 📄 VIVA_PREPARATION_GUIDE.md    ✅ Read this!
├─── 📄 VIVA_QUICK_REFERENCE.md      ✅ Print this!
├─── 📄 VIVA_VISUAL_DIAGRAMS.md      ✅ Study this!
│
├─── 🐍 run.py                       (GUI entry)
├─── 🐍 app/main.py                  (CLI entry)
│
├─── 📁 app/config/
│    └─── ⚙️ settings.py             (All constants here!)
│
├─── 📁 app/controllers/
│    ├─── 🎮 auth_controller.py
│    ├─── 🎮 attendance_controller.py
│    ├─── 🎮 registration_controller.py
│    └─── 🎮 training_controller.py
│
├─── 📁 app/services/                 (⭐ CORE LOGIC)
│    ├─── ⭐ face_recognition_service.py
│    ├─── ⭐ training_service.py
│    ├─── ⭐ registration_service.py
│    └─── attendance_service.py
│
├─── 📁 app/models/
│    ├─── 📦 employee.py
│    ├─── 📦 employee_repository.py
│    └─── 📦 admin_repository.py
│
├─── 📁 app/database/
│    └─── 🗄️ db.py                  (Database init)
│
├─── 📁 app/presentation/gui/
│    ├─── 🖼️ login_window.py
│    ├─── 🖼️ dashboard_window.py
│    ├─── 🖼️ attendance_window.py
│    └─── 🖼️ (other windows)
│
├─── 📁 dataset/
│    ├─── 📷 1/  (Employee 1 samples)
│    ├─── 📷 2/  (Employee 2 samples)
│    └─── 📷 N/
│
├─── 📁 models_storage/
│    └─── 🤖 trainer.yml            (Trained LBPH model)
│
├─── 📊 attendance.db               (SQLite database)
├─── 📋 requirements.txt
└─── 📖 README.md
```

---

**Use these diagrams to explain complex concepts during your viva! 🎓**

