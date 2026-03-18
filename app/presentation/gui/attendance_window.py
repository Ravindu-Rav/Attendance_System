from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QSizePolicy,
)
from PySide6.QtGui import QColor, QCursor, QImage, QPixmap
from PySide6.QtCore import Qt, QTimer, QThread, Signal
import cv2
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.services.training_service import train_model
from app.services.face_recognition_service import get_employee_name
from app.database.db import get_connection
from datetime import datetime


class CameraThread(QThread):
    frame_ready = Signal(QImage)
    recognition_result = Signal(str, str)  # name, status
    model_status = Signal(str)  # human message about model status

    def __init__(self):
        super().__init__()
        self.running = False
        self.recognizer = None
        self.face_cascade = None
        self.model_loaded = False
        self._model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
            'models_storage',
            'trainer.yml'
        )
        self._load_attempt_counter = 0

        # Prevent repeated marking in quick succession
        self._last_recognized_id = None
        self._last_recognized_time = None
        self._recognition_cooldown_seconds = 5

        # Track who has been marked today so we avoid repeated DB checks and UI updates
        self._marked_today = set()
        self._marked_today_date = None
        self._already_notified_marked = set()
    def try_load_model(self):
        """Attempt to load the trained model file.

        This is called repeatedly while scanning so that if the model appears
        later (after training), the system will start recognizing without needing
        to restart the app.
        """
        if self.model_loaded:
            return

        exists = os.path.exists(self._model_path)
        size = os.path.getsize(self._model_path) if exists else 0
        status_msg = f"Checking model: exists={exists}, size={size}"
        print(status_msg)
        self.model_status.emit(status_msg)

        if exists and size > 0:
            try:
                if self.recognizer is None:
                    self.recognizer = cv2.face.LBPHFaceRecognizer_create()

                self.recognizer.read(self._model_path)
                self.model_loaded = True
                msg = "Model loaded successfully"
                print(msg)
                self.model_status.emit(msg)
            except Exception as e:
                msg = f"Failed to load model: {e}"
                print(msg)
                self.model_status.emit(msg)
                self.model_loaded = False
        else:
            # If file isn't present yet, keep trying periodically
            msg = "Model file not found or empty"
            print(msg)
            self.model_status.emit(msg)
            self.model_loaded = False

    def run(self):
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )

            cam = cv2.VideoCapture(0)
            self.running = True

            while self.running:
                ret, frame = cam.read()
                if not ret:
                    continue

                # Periodically attempt to load model if it isn't loaded yet
                self._load_attempt_counter += 1
                if self._load_attempt_counter % 30 == 0:
                    self.try_load_model()

                # Process frame for recognition
                self._process_frame(frame)

                # Convert to QImage for display
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.frame_ready.emit(qt_image)

                self.msleep(30)  # ~30 FPS

            cam.release()

        except Exception as e:
            print(f"Camera error: {e}")

    def _process_frame(self, frame):
        if not self.face_cascade:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        # Reset per-day tracking when the date changes
        today = datetime.now().strftime("%Y-%m-%d")
        if self._marked_today_date != today:
            self._marked_today_date = today
            self._marked_today.clear()
            self._already_notified_marked.clear()
            self._last_recognized_id = None
            self._last_recognized_time = None

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            if self.model_loaded and self.recognizer:
                face = gray[y:y+h, x:x+w]
                try:
                    employee_id, confidence = self.recognizer.predict(face)

                    if confidence < 60:  # Confidence threshold
                        employee = get_employee_name(employee_id)
                        if employee:
                            name = f"{employee[0]} {employee[1]}"

                            if employee_id in self._marked_today:
                                # Already recorded for today; notify once and avoid spamming UI
                                status = "Already Marked"
                                if employee_id not in self._already_notified_marked:
                                    self.recognition_result.emit(name, status)
                                    self._already_notified_marked.add(employee_id)
                            else:
                                now = datetime.now()
                                if (
                                    self._last_recognized_id == employee_id
                                    and self._last_recognized_time
                                    and (now - self._last_recognized_time).total_seconds() < self._recognition_cooldown_seconds
                                ):
                                    status = "Recognizing..."
                                else:
                                    status = self._mark_attendance(employee_id)
                                    self._last_recognized_id = employee_id
                                    self._last_recognized_time = now

                                    if status in ("Marked ✓", "Already Marked"):
                                        self._marked_today.add(employee_id)

                                    self.recognition_result.emit(name, status)

                            # Draw on frame
                            cv2.putText(frame, f"{name} ({status})", (x, y-30),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        else:
                            cv2.putText(frame, "Unknown Employee", (x, y-30),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    else:
                        cv2.putText(frame, "Unknown", (x, y-30),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                except Exception as e:
                    print(f"Recognition error: {e}")
                    cv2.putText(frame, "Recognition Error", (x, y-30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Model Not Trained", (x, y-30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 165, 0), 2)

    def _mark_attendance(self, employee_id):
        try:
            conn = get_connection()
            c = conn.cursor()

            today = datetime.now().strftime("%Y-%m-%d")

            # Check if already marked
            c.execute("SELECT * FROM On_Duty WHERE employee_ID=? AND date=?",
                     (employee_id, today))
            if c.fetchone():
                conn.close()
                return "Already Marked"

            # Mark attendance
            c.execute("""
                INSERT INTO On_Duty(employee_ID, duration, date)
                VALUES(?, ?, ?)
            """, (employee_id, 8, today))

            conn.commit()
            conn.close()
            return "Marked ✓"

        except Exception as e:
            print(f"Attendance marking error: {e}")
            return "Error"

    def stop(self):
        self.running = False
        self.wait()


class AttendanceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System — Mark Attendance")
        self.setMinimumSize(600, 600)
        self.resize(600, 600)

        self.camera_thread = None
        self.is_scanning = False

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self._build_ui()
        self._apply_styles()
        self._connect_signals()
        self._load_today_attendance()
        self.status_label.hide()  # Hide initially

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

        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        self.title = QLabel("Mark Attendance")
        self.title.setObjectName("title")
        self.subtitle = QLabel("Live recognition and attendance log")
        self.subtitle.setObjectName("subtitle")
        title_layout.addWidget(self.title)
        title_layout.addWidget(self.subtitle)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self._back_to_main)
        header_layout.addWidget(self.back_button)

        card_layout.addLayout(header_layout)

        # Camera Feed
        self.camera_label = QLabel("Camera not started")
        self.camera_label.setObjectName("cameraLabel")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setFixedHeight(300)
        self.camera_label.setStyleSheet("background-color: #2b2b2b; border-radius: 10px; color: #bbbbbb; font-size: 18px; border: 2px dashed #444;")
        card_layout.addWidget(self.camera_label)

        # Mark Button
        self.mark_button = QPushButton("Start Attendance Scanning")
        self.mark_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.mark_button.setObjectName("markButton")
        card_layout.addWidget(self.mark_button)

        # Today's Attendance List
        self.attendance_list = QListWidget()
        self.attendance_list.setObjectName("attendanceList")
        card_layout.addWidget(self.attendance_list)

        # Status Label
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.status_label)

        main_layout.addStretch()
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.card)
        h_layout.addStretch()
        main_layout.addLayout(h_layout)
        main_layout.addStretch()

    def _connect_signals(self):
        """Connect button signals"""
        self.mark_button.clicked.connect(self._toggle_attendance_scanning)

    def _toggle_attendance_scanning(self):
        """Start or stop attendance scanning"""
        if not self.is_scanning:
            self._start_scanning()
        else:
            self._stop_scanning()

    def _start_scanning(self):
        """Start camera and face recognition"""
        try:
            self.status_label.setText("Starting camera...")
            self.status_label.show()

            self.camera_thread = CameraThread()
            self.camera_thread.frame_ready.connect(self._update_camera_feed)
            self.camera_thread.recognition_result.connect(self._handle_recognition_result)
            self.camera_thread.model_status.connect(self._update_model_status)
            self.camera_thread.start()
            # immediately attempt to load any existing model
            self.camera_thread.try_load_model()

            self.is_scanning = True
            self.mark_button.setText("Stop Scanning")
            self.mark_button.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    padding: 15px;
                    border-radius: 12px;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
                QPushButton:pressed {
                    background-color: #bd2130;
                }
            """)

            # Check if model is loaded after a short delay
            QTimer.singleShot(1500, self._check_model_status)

        except Exception as e:
            QMessageBox.critical(self, "Camera Error", f"Failed to start camera: {str(e)}")
            self.status_label.setText("Error starting camera")
            self.status_label.show()

    def _check_model_status(self):
        """Check if the recognition model is loaded and show appropriate message"""
        if hasattr(self.camera_thread, 'model_loaded') and not self.camera_thread.model_loaded:
            self.status_label.setText("Model not loaded (waiting for model file)...")
            reply = QMessageBox.question(
                self,
                "Model Not Trained",
                "The face recognition model is missing or not properly trained.\n\n"
                "Would you like to train it now?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )

            self._stop_scanning()

            if reply == QMessageBox.Yes:
                self._retrain_model()
        else:
            self.status_label.setText("Model loaded, ready for recognition")


    def _retrain_model(self):
        """Retrain the face recognition model"""
        try:
            self.status_label.setText("Training model... Please wait...")
            self.status_label.show()

            # Run training in a separate thread to avoid blocking UI
            from PySide6.QtCore import QThread, Signal

            class TrainingThread(QThread):
                finished = Signal(bool, str)

                def run(self):
                    try:
                        success = train_model()
                        if success:
                            self.finished.emit(True, "Model trained successfully!")
                        else:
                            self.finished.emit(False, "Failed to train model. No training data found.")
                    except Exception as e:
                        self.finished.emit(False, f"Training error: {str(e)}")

            self.training_thread = TrainingThread()
            self.training_thread.finished.connect(self._on_training_finished)
            self.training_thread.start()

        except Exception as e:
            QMessageBox.critical(self, "Training Error", f"Failed to start training: {str(e)}")
            self.status_label.setText("Ready")

    def _on_training_finished(self, success, message):
        """Handle training completion"""
        if success:
            QMessageBox.information(self, "Training Complete", message)
            # Restart camera thread to reload the new model
            if self.is_scanning:
                self._stop_scanning()
                QTimer.singleShot(500, self._start_scanning)
        else:
            QMessageBox.warning(self, "Training Failed", message)

        self.status_label.hide()

    def _stop_scanning(self):
        """Stop camera and face recognition"""
        if self.camera_thread:
            self.camera_thread.stop()
            self.camera_thread = None

        self.is_scanning = False
        self.mark_button.setText("Start Attendance Scanning")
        self.camera_label.setText("Camera stopped")
        self._reset_mark_button_style()

    def _reset_mark_button_style(self):
        """Reset mark button to original style"""
        self.mark_button.setStyleSheet("""
            QPushButton#markButton {
                background-color: #16c2ff;
                color: #0b1216;
                padding: 15px;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton#markButton:hover {
                background-color: #0fb4e6;
            }
            QPushButton#markButton:pressed {
                background-color: #0a9bc7;
            }
        """)

    def _update_camera_feed(self, image):
        """Update camera feed display"""
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(self.camera_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.camera_label.setPixmap(scaled_pixmap)

    def _handle_recognition_result(self, name, status):
        """Handle face recognition result"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        item_text = f"{name} - {timestamp} ({status})"

        # Update status label
        self.status_label.setText(f"Last recognized: {name} ({status})")
        self.status_label.show()

        # Add to list if not already present today
        already_present = False
        for i in range(self.attendance_list.count()):
            if name in self.attendance_list.item(i).text():
                already_present = True
                break

        if not already_present:
            self.attendance_list.addItem(item_text)

        # Show notification only when a new attendance mark is recorded
        if status == "Marked ✓":
            QMessageBox.information(self, "Attendance Marked", f"Attendance marked for {name}")

    def _update_model_status(self, msg):
        """Update model status message from the camera thread"""
        self.status_label.setText(msg)
        self.status_label.show()

    def _load_today_attendance(self):
        """Load today's attendance records"""
        try:
            conn = get_connection()
            c = conn.cursor()

            today = datetime.now().strftime("%Y-%m-%d")
            c.execute("""
                SELECT e.fname, e.lname, o.date
                FROM On_Duty o
                JOIN Employee e ON o.employee_ID = e.employee_ID
                WHERE o.date = ?
                ORDER BY o.date DESC
            """, (today,))

            self.attendance_list.clear()
            for row in c.fetchall():
                name = f"{row[0]} {row[1]}"
                self.attendance_list.addItem(f"{name} - Today")

            conn.close()

        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Failed to load attendance: {str(e)}")

    def _back_to_main(self):
        """Go back to main menu"""
        if self.is_scanning:
            self._stop_scanning()

        from .main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def closeEvent(self, event):
        """Handle window close event"""
        if self.is_scanning:
            self._stop_scanning()
        event.accept()

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

        QLabel#subtitle {
            font-size: 13px;
            color: #9aa6ac;
        }

        /* Camera Label */
        QLabel#cameraLabel {
            background-color: rgba(16, 20, 24, 0.8);
            border-radius: 12px;
            color: #aab4ba;
            font-size: 18px;
            border: 2px dashed rgba(255, 255, 255, 0.12);
        }

        /* Mark Button */
        QPushButton#markButton {
            background-color: #16c2ff;
            color: #0b1216;
            padding: 15px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
        }

        QPushButton#markButton:hover {
            background-color: #0fb4e6;
        }

        QPushButton#markButton:pressed {
            background-color: #0a9bc7;
        }

        /* Attendance List */
        QListWidget#attendanceList {
            background-color: rgba(16, 20, 24, 0.8);
            border-radius: 12px;
            padding: 10px;
            color: #e8edf1;
            font-size: 14px;
        }

        QListWidget#attendanceList::item {
            padding: 5px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        QListWidget#attendanceList::item:selected {
            background-color: #16c2ff;
            color: #0b1216;
        }

        /* Back Button */
        QPushButton#backButton {
            background-color: rgba(255, 255, 255, 0.08);
            color: #e8edf1;
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
        }

        QPushButton#backButton:hover {
            background-color: rgba(255, 255, 255, 0.14);
        }

        QPushButton#backButton:pressed {
            background-color: rgba(255, 255, 255, 0.2);
        }

        /* Status Label */
        QLabel#statusLabel {
            color: #c2c9ce;
            font-size: 14px;
            padding: 5px;
            background-color: rgba(22, 26, 30, 0.8);
            border-radius: 5px;
        }
        """)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AttendanceWindow()
    window.show()
    sys.exit(app.exec())
