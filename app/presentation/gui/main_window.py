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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System — Main Menu")
        self.setFixedSize(420, 560)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self._build_ui()
        self._apply_styles()
        self._connect_signals()

    def _connect_signals(self):
        """Connect button signals"""
        self.dashboard_button.clicked.connect(self._open_dashboard)
        self.employee_button.clicked.connect(self._open_employee_management)
        self.attendance_button.clicked.connect(self._open_attendance)
        self.logout_button.clicked.connect(self._logout)

    def _open_dashboard(self):
        """Open dashboard window"""
        from .dashboard_window import DashboardWindow
        self.dashboard_window = DashboardWindow()
        self.dashboard_window.show()
        self.close()

    def _open_employee_management(self):
        """Open employee management window"""
        from .employee_window import EmployeeWindow
        self.employee_window = EmployeeWindow()
        self.employee_window.show()
        self.close()

    def _open_attendance(self):
        """Open attendance window"""
        from .attendance_window import AttendanceWindow
        self.attendance_window = AttendanceWindow()
        self.attendance_window.show()
        self.close()

    def _logout(self):
        """Logout and return to login"""
        from .login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

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
        self.title = QLabel("Attendance System")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        self.subtitle = QLabel("Main Menu")
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.subtitle)

        # Buttons
        self.dashboard_button = QPushButton("Dashboard")
        self.dashboard_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.dashboard_button.setObjectName("menuButton")
        card_layout.addWidget(self.dashboard_button)

        self.employee_button = QPushButton("Manage Employees")
        self.employee_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.employee_button.setObjectName("menuButton")
        card_layout.addWidget(self.employee_button)

        self.attendance_button = QPushButton("Mark Attendance")
        self.attendance_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.attendance_button.setObjectName("menuButton")
        card_layout.addWidget(self.attendance_button)

        self.logout_button = QPushButton("Logout")
        self.logout_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.logout_button.setObjectName("logoutButton")
        card_layout.addWidget(self.logout_button)

        main_layout.addStretch()
        main_layout.addWidget(self.card)
        main_layout.addStretch()

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

        QLabel#subtitle {
            font-size: 14px;
            color: #bbbbbb;
            margin-bottom: 10px;
        }

        /* Menu Buttons */
        QPushButton#menuButton {
            background-color: #00c6ff;
            color: black;
            padding: 12px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
        }

        QPushButton#menuButton:hover {
            background-color: #00a6d6;
        }

        QPushButton#menuButton:pressed {
            background-color: #008bb5;
        }

        /* Logout Button */
        QPushButton#logoutButton {
            background-color: #ff4444;
            color: white;
            padding: 12px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
        }

        QPushButton#logoutButton:hover {
            background-color: #cc3333;
        }

        QPushButton#logoutButton:pressed {
            background-color: #aa2222;
        }
        """)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
