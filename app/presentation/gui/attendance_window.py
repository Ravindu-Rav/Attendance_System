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
)
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt


class AttendanceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System — Mark Attendance")
        self.setFixedSize(600, 600)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Card container
        self.card = QFrame()
        self.card.setObjectName("card")

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
        self.title = QLabel("Mark Attendance")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        # Camera Placeholder
        self.camera_label = QLabel("Camera Feed Here")
        self.camera_label.setObjectName("cameraLabel")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setFixedHeight(200)
        card_layout.addWidget(self.camera_label)

        # Mark Button
        self.mark_button = QPushButton("Mark Attendance")
        self.mark_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.mark_button.setObjectName("markButton")
        card_layout.addWidget(self.mark_button)

        # Today's Attendance List
        self.attendance_list = QListWidget()
        self.attendance_list.setObjectName("attendanceList")
        # Placeholder items
        self.attendance_list.addItem("John Doe - 08:30 AM")
        self.attendance_list.addItem("Jane Smith - 08:45 AM")
        card_layout.addWidget(self.attendance_list)

        # Back Button
        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self._back_to_main)
        card_layout.addWidget(self.back_button)

        main_layout.addStretch()
        main_layout.addWidget(self.card)
        main_layout.addStretch()

    def _back_to_main(self):
        """Go back to main menu"""
        from .main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

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
            background-color: rgba(25, 25, 25, 0.95);
            border-radius: 20px;
        }

        /* Title */
        QLabel#title {
            font-size: 26px;
            font-weight: bold;
            color: #ffffff;
        }

        /* Camera Label */
        QLabel#cameraLabel {
            background-color: #2b2b2b;
            border-radius: 10px;
            color: #bbbbbb;
            font-size: 18px;
            border: 2px dashed #444;
        }

        /* Mark Button */
        QPushButton#markButton {
            background-color: #00c6ff;
            color: black;
            padding: 15px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
        }

        QPushButton#markButton:hover {
            background-color: #00a6d6;
        }

        QPushButton#markButton:pressed {
            background-color: #008bb5;
        }

        /* Attendance List */
        QListWidget#attendanceList {
            background-color: #2b2b2b;
            border-radius: 10px;
            padding: 10px;
            color: white;
            font-size: 14px;
        }

        QListWidget#attendanceList::item {
            padding: 5px;
            border-bottom: 1px solid #444;
        }

        QListWidget#attendanceList::item:selected {
            background-color: #00c6ff;
            color: black;
        }

        /* Back Button */
        QPushButton#backButton {
            background-color: #444;
            color: white;
            padding: 12px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
        }

        QPushButton#backButton:hover {
            background-color: #555;
        }

        QPushButton#backButton:pressed {
            background-color: #666;
        }
        """)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AttendanceWindow()
    window.show()
    sys.exit(app.exec())
