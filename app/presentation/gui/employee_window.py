from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QProgressBar,
    QTextEdit,
    QSizePolicy,
)
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt, QThread, Signal
import sys
import os
import cv2
import numpy as np


class FaceCaptureThread(QThread):
    """Thread for capturing faces"""
    progress = Signal(str)
    finished = Signal(bool, str)

    def __init__(self, employee_id, num_samples=30):
        super().__init__()
        self.employee_id = employee_id
        self.num_samples = num_samples

    def run(self):
        """Run face capture in thread"""
        try:
            self.progress.emit("Initializing camera...")
            dataset_path = os.path.join("dataset", str(self.employee_id))
            os.makedirs(dataset_path, exist_ok=True)

            face_detector = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )

            cam = cv2.VideoCapture(0)
            count = 0

            self.progress.emit(f"Capturing {self.num_samples} face samples...")

            while count < self.num_samples:
                ret, img = cam.read()
                if not ret:
                    self.finished.emit(False, "Failed to capture frame from camera")
                    return

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    if count < self.num_samples:
                        count += 1
                        face = gray[y:y+h, x:x+w]
                        file_path = os.path.join(dataset_path, f"{count}.jpg")
                        cv2.imwrite(file_path, face)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        cv2.putText(img, f"Samples: {count}/{self.num_samples}", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        self.progress.emit(f"Captured sample {count}/{self.num_samples}")
                        break  # Capture one face per frame

                cv2.imshow("Capturing Faces - Press ESC to cancel", img)

                if cv2.waitKey(1) == 27:  # ESC key
                    cam.release()
                    cv2.destroyAllWindows()
                    self.finished.emit(False, "Capture cancelled by user")
                    return

            cam.release()
            cv2.destroyAllWindows()
            self.finished.emit(True, f"Successfully captured {count} face samples")

        except Exception as e:
            self.finished.emit(False, str(e))


class ModelTrainingThread(QThread):
    """Thread for training model"""
    progress = Signal(str)
    finished = Signal(bool, str)

    def run(self):
        """Run training in thread"""
    def run(self):
        """Run training in thread"""
        try:
            from app.controllers.training_controller import handle_train_model
            success = handle_train_model()
            if success:
                self.finished.emit(True, "Model training completed successfully!")
            else:
                self.finished.emit(False, "No training data found. Please capture faces for employees first.")
        except Exception as e:
            self.finished.emit(False, str(e))


class EmployeeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System — Manage Employees")
        self.setMinimumSize(350, 450)
        self.resize(420, 560)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self._build_ui()
        self._apply_styles()
        self._connect_signals()
        self._load_employees()
        self._load_departments()

    def _connect_signals(self):
        """Connect button signals"""
        self.add_button.clicked.connect(self._add_employee)
        self.edit_button.clicked.connect(self._edit_employee)
        self.delete_button.clicked.connect(self._delete_employee)
        self.capture_button.clicked.connect(self._capture_faces)
        self.back_button.clicked.connect(self._back_to_main)
        self.employee_list.itemSelectionChanged.connect(self._on_employee_selected)

    def _build_ui(self):
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Card container
        self.card = QFrame()
        self.card.setObjectName("card")
        self.card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 50, 40, 40)
        card_layout.setSpacing(20)

        # Title
        self.title = QLabel("Manage Employees")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        # Employee List
        self.employee_list = QListWidget()
        self.employee_list.setObjectName("employeeList")
        card_layout.addWidget(self.employee_list)

        # Add Employee Form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Employee Name")
        self.name_input.setObjectName("input")
        form_layout.addWidget(self.name_input)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Employee ID")
        self.id_input.setObjectName("input")
        form_layout.addWidget(self.id_input)

        self.department_combo = QComboBox()
        self.department_combo.setObjectName("input")
        form_layout.addWidget(self.department_combo)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Employee")
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_button.setObjectName("addButton")
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.edit_button.setObjectName("editButton")
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.delete_button.setObjectName("deleteButton")
        button_layout.addWidget(self.delete_button)

        form_layout.addLayout(button_layout)
        card_layout.addLayout(form_layout)

        # Face Capture and Training Section
        capture_layout = QVBoxLayout()
        capture_layout.setSpacing(10)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setVisible(False)
        capture_layout.addWidget(self.progress_bar)

        # Status Text
        self.status_text = QTextEdit()
        self.status_text.setObjectName("statusText")
        self.status_text.setReadOnly(True)
        self.status_text.setFixedHeight(80)
        self.status_text.setVisible(False)
        capture_layout.addWidget(self.status_text)

        # Capture and Train Buttons
        action_layout = QHBoxLayout()
        self.capture_button = QPushButton("Capture Faces for Selected Employee")
        self.capture_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.capture_button.setObjectName("captureButton")
        self.capture_button.setEnabled(False)  # Disabled until employee selected
        action_layout.addWidget(self.capture_button)

        capture_layout.addLayout(action_layout)
        card_layout.addLayout(capture_layout)

        # Back Button
        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self._back_to_main)
        card_layout.addWidget(self.back_button)

        main_layout.addStretch()
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.card)
        h_layout.addStretch()
        main_layout.addLayout(h_layout)
        main_layout.addStretch()

    def _back_to_main(self):
        """Go back to main menu"""
        from .main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def _load_employees(self):
        """Load employees from database"""
        self.employee_list.clear()
        try:
            from app.controllers.registration_controller import handle_get_employees
            employees = handle_get_employees()
            for emp in employees:
                dept = emp[3] if len(emp) > 3 and emp[3] else "No Department"
                self.employee_list.addItem(f"{emp[1]} {emp[2]} - ID: {emp[0]} ({dept})")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load employees: {str(e)}")

    def _load_departments(self):
        """Load departments into dropdown"""
        self.department_combo.clear()
        self.department_combo.addItem("Select Department", None)
        try:
            from app.database.db import get_connection
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT dept_ID, department_name FROM Department ORDER BY department_name")
            for dept_id, name in cur.fetchall():
                self.department_combo.addItem(name, dept_id)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load departments: {str(e)}")
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def _add_employee(self):
        """Add new employee"""
        name = self.name_input.text().strip()
        emp_id = self.id_input.text().strip()
        dept_id = self.department_combo.currentData()

        if not name or not emp_id:
            QMessageBox.warning(self, "Error", "Please enter both name and ID")
            return

        if dept_id is None:
            QMessageBox.warning(self, "Error", "Please select a department")
            return

        try:
            from app.controllers.registration_controller import handle_add_employee
            handle_add_employee(name, emp_id, dept_id)
            QMessageBox.information(self, "Success", f"Employee {name} added successfully!")
            self.name_input.clear()
            self.id_input.clear()
            self.department_combo.setCurrentIndex(0)
            self._load_employees()

            # Automatically start face capture for the new employee
            reply = QMessageBox.question(self, "Face Capture",
                                       f"Do you want to capture faces for {name} now?",
                                       QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                self._capture_faces_for_employee(int(emp_id))

        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add employee: {str(e)}")

    def _edit_employee(self):
        """Edit selected employee"""
        current_item = self.employee_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select an employee to edit")
            return

        # Parse employee ID from text
        text = current_item.text()
        emp_id = self._extract_employee_id(text)
        if not emp_id:
            QMessageBox.warning(self, "Error", "Could not determine employee ID")
            return

        new_name = self.name_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Error", "Please enter new name")
            return

        try:
            from app.controllers.registration_controller import handle_update_employee
            handle_update_employee(emp_id, new_name)
            QMessageBox.information(self, "Success", "Employee updated successfully!")
            self._load_employees()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update employee: {str(e)}")

    def _delete_employee(self):
        """Delete selected employee"""
        current_item = self.employee_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select an employee to delete")
            return

        text = current_item.text()
        emp_id = self._extract_employee_id(text)
        if not emp_id:
            QMessageBox.warning(self, "Error", "Could not determine employee ID")
            return

        reply = QMessageBox.question(self, "Confirm Delete",
                                   f"Are you sure you want to delete employee {text}?",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                from app.controllers.registration_controller import handle_delete_employee
                handle_delete_employee(emp_id)
                QMessageBox.information(self, "Success", "Employee deleted successfully!")
                self._load_employees()
                self.capture_button.setEnabled(False)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete employee: {str(e)}")

    def _capture_faces_for_employee(self, emp_id):
        """Capture faces for a specific employee ID"""
        self.progress_bar.setVisible(True)
        self.status_text.setVisible(True)
        self.status_text.clear()

        self.capture_thread = FaceCaptureThread(emp_id)
        self.capture_thread.progress.connect(self._update_capture_progress)
        self.capture_thread.finished.connect(self._capture_finished_and_train)
        self.capture_thread.start()

    def _capture_faces(self):
        """Capture faces for selected employee"""
        current_item = self.employee_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select an employee first")
            return

        text = current_item.text()
        emp_id_text = self._extract_employee_id(text)
        if not emp_id_text:
            QMessageBox.warning(self, "Error", "Could not determine employee ID")
            return
        emp_id = int(emp_id_text)

        reply = QMessageBox.question(self, "Face Capture",
                                   f"Do you want to capture faces for {text}?",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self._capture_faces_for_employee(emp_id)

    def _train_model(self):
        """Train the face recognition model"""
        self.progress_bar.setVisible(True)
        self.status_text.setVisible(True)
        self.status_text.clear()
        self.train_button.setEnabled(False)

        self.train_thread = ModelTrainingThread()
        self.train_thread.progress.connect(self._update_train_progress)
        self.train_thread.finished.connect(self._train_finished)
        self.train_thread.start()

    def _update_capture_progress(self, text):
        """Update capture progress"""
        self.status_text.append(text)

    def _capture_finished_and_train(self, success, message):
        """Handle capture completion and start training"""
        if success:
            QMessageBox.information(self, "Success", message + "\n\nStarting model training...")
            self._start_training()
        else:
            QMessageBox.warning(self, "Error", message)
            self.progress_bar.setVisible(False)

    def _start_training(self):
        """Start the training process"""
        self.status_text.append("Starting model training...")

        self.train_thread = ModelTrainingThread()
        self.train_thread.progress.connect(self._update_train_progress)
        self.train_thread.finished.connect(self._training_completed)
        self.train_thread.start()

    def _update_train_progress(self, text):
        """Update training progress"""
        self.status_text.append(text)

    def _training_completed(self, success, message):
        """Handle training completion"""
        self.progress_bar.setVisible(False)
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", message)

    def _on_employee_selected(self):
        """Enable capture button when employee is selected"""
        self.capture_button.setEnabled(self.employee_list.currentItem() is not None)

    def _extract_employee_id(self, text):
        """Extract employee ID from list item text"""
        try:
            return text.split("ID: ")[1].split(" ")[0]
        except Exception:
            return None

    def _apply_styles(self):
        self.setStyleSheet("""
        /* Dark Gradient Background */
        QMainWindow {
            background: qlineargradient(
                spread:pad,
                x1:0, y1:0,
                x2:1, y2:1,
                stop:0 #0f2027,
                stop:1 #203a43
            );
        }

        /* Card */
        QFrame#card {
            background: qlineargradient(
                spread:pad,
                x1:0, y1:0,
                x2:0, y2:1,
                stop:0 rgba(30, 34, 38, 0.98),
                stop:1 rgba(22, 24, 28, 0.98)
            );
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 24px;
            max-width: 1200px;
        }

        /* Title */
        QLabel#title {
            font-size: 28px;
            font-weight: 700;
            color: #f4f7f9;
            letter-spacing: 0.3px;
        }

        /* Employee List */
        QListWidget#employeeList {
            background-color: rgba(16, 20, 24, 0.8);
            border-radius: 12px;
            padding: 10px;
            color: #e8edf1;
            font-size: 14px;
        }

        QListWidget#employeeList::item {
            padding: 5px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        QListWidget#employeeList::item:selected {
            background-color: #16c2ff;
            color: #0b1216;
        }

        /* Inputs */
        QLineEdit#input, QComboBox#input {
            padding: 12px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            font-size: 14px;
            background-color: rgba(16, 20, 24, 0.9);
            color: #e8edf1;
        }

        QLineEdit#input:focus, QComboBox#input:focus {
            border: 2px solid #16c2ff;
            background-color: rgba(22, 26, 30, 0.95);
        }

        /* Buttons */
        QPushButton#addButton {
            background-color: #16c2ff;
            color: #0b1216;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
        }

        QPushButton#addButton:hover {
            background-color: #0fb4e6;
        }

        QPushButton#editButton {
            background-color: #f5b342;
            color: #0b1216;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
        }

        QPushButton#editButton:hover {
            background-color: #e2a63a;
        }

        QPushButton#deleteButton {
            background-color: #ff4b55;
            color: #ffffff;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
        }

        QPushButton#deleteButton:hover {
            background-color: #e13e47;
        }

        /* Progress Bar */
        QProgressBar#progressBar {
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 5px;
            text-align: center;
        }

        QProgressBar#progressBar::chunk {
            background-color: #16c2ff;
        }

        /* Status Text */
        QTextEdit#statusText {
            background-color: rgba(16, 20, 24, 0.9);
            border-radius: 5px;
            padding: 5px;
            color: #e8edf1;
            font-family: monospace;
            font-size: 11px;
        }

        /* Capture Button */
        QPushButton#captureButton {
            background-color: #f5b342;
            color: #0b1216;
            padding: 10px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: bold;
        }

        QPushButton#captureButton:hover {
            background-color: #e2a63a;
        }

        QPushButton#captureButton:pressed {
            background-color: #c89132;
        }

        QPushButton#captureButton:disabled {
            background-color: #525a61;
            color: #c2c9ce;
        }

        QPushButton#backButton {
            background-color: rgba(255, 255, 255, 0.08);
            color: #e8edf1;
            padding: 12px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
        }

        QPushButton#backButton:hover {
            background-color: rgba(255, 255, 255, 0.14);
        }
        """)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = EmployeeWindow()
    window.show()
    sys.exit(app.exec())
