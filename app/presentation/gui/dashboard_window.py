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
)
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System — Dashboard")
        self.setFixedSize(600, 500)

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
        card_layout.setSpacing(25)

        # Title
        self.title = QLabel("Dashboard")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        # Stats
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        # Total Employees
        emp_frame = QFrame()
        emp_frame.setObjectName("statFrame")
        emp_layout = QVBoxLayout(emp_frame)
        emp_title = QLabel("Total Employees")
        emp_title.setObjectName("statTitle")
        emp_value = QLabel("150")  # Placeholder
        emp_value.setObjectName("statValue")
        emp_layout.addWidget(emp_title)
        emp_layout.addWidget(emp_value)
        stats_layout.addWidget(emp_frame)

        # Today's Attendance
        att_frame = QFrame()
        att_frame.setObjectName("statFrame")
        att_layout = QVBoxLayout(att_frame)
        att_title = QLabel("Today's Attendance")
        att_title.setObjectName("statTitle")
        att_value = QLabel("120")  # Placeholder
        att_value.setObjectName("statValue")
        att_layout.addWidget(att_title)
        att_layout.addWidget(att_value)
        stats_layout.addWidget(att_frame)

        # Absent Today
        abs_frame = QFrame()
        abs_frame.setObjectName("statFrame")
        abs_layout = QVBoxLayout(abs_frame)
        abs_title = QLabel("Absent Today")
        abs_title.setObjectName("statTitle")
        abs_value = QLabel("30")  # Placeholder
        abs_value.setObjectName("statValue")
        abs_layout.addWidget(abs_title)
        abs_layout.addWidget(abs_value)
        stats_layout.addWidget(abs_frame)

        card_layout.addLayout(stats_layout)

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

        /* Stat Frames */
        QFrame#statFrame {
            background-color: #2b2b2b;
            border-radius: 10px;
            padding: 20px;
            min-width: 120px;
        }

        QLabel#statTitle {
            font-size: 14px;
            color: #bbbbbb;
            text-align: center;
        }

        QLabel#statValue {
            font-size: 24px;
            font-weight: bold;
            color: #00c6ff;
            text-align: center;
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
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())
