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
    QSizePolicy,
    QStatusBar,
)
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System — Main Menu")
        self.setMinimumSize(420, 560)
        self.resize(420, 560)

        self.setWindowState(Qt.WindowMaximized)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self._build_ui()
        self._apply_styles()
        self._connect_signals()
        self._setup_status_bar()
        self._setup_shortcuts()

    def _connect_signals(self):
        """Connect button signals"""
        self.dashboard_button.clicked.connect(self._open_dashboard)
        self.employee_button.clicked.connect(self._open_employee_management)
        self.attendance_button.clicked.connect(self._open_attendance)
        self.logout_button.clicked.connect(self._logout)

    def _setup_status_bar(self):
        """Setup status bar with system information"""
        self.status_bar = self.statusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: rgba(25, 25, 25, 0.95);
                color: #cccccc;
                border-top: 1px solid #444;
            }
        """)

        # Add status labels
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #cccccc; padding: 2px;")
        self.status_bar.addWidget(self.status_label)

        self.status_bar.addPermanentWidget(QLabel("Attendance System v1.0"))
        self.status_bar.showMessage("System ready", 3000)

    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        from PySide6.QtGui import QShortcut
        from PySide6.QtCore import Qt

        # Ctrl+D for Dashboard
        QShortcut(Qt.CTRL | Qt.Key_D, self, self._open_dashboard)

        # Ctrl+E for Employee Management
        QShortcut(Qt.CTRL | Qt.Key_E, self, self._open_employee_management)

        # Ctrl+A for Attendance
        QShortcut(Qt.CTRL | Qt.Key_A, self, self._open_attendance)

        # Ctrl+Q to quit
        QShortcut(Qt.CTRL | Qt.Key_Q, self, self._confirm_quit)

    def _confirm_quit(self):
        """Confirm before quitting"""
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, "Confirm Exit",
            "Are you sure you want to exit the Attendance System?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()

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
        self.login_window.showMaximized()
        self.close()

    def _build_ui(self):
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Card container
        self.card = QFrame()
        self.card.setObjectName("card")
        self.card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.card.setMinimumWidth(900)

        # Drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(64, 60, 64, 56)
        card_layout.setSpacing(18)

        # Title
        self.title = QLabel("Attendance System")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        self.subtitle = QLabel("Main Menu")
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.subtitle)

        self.caption = QLabel("Choose an action to continue")
        self.caption.setObjectName("caption")
        self.caption.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.caption)

        # Buttons
        self.dashboard_button = QPushButton("Dashboard")
        self.dashboard_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.dashboard_button.setObjectName("menuButton")
        self.dashboard_button.setToolTip("View system dashboard (Ctrl+D)")
        card_layout.addWidget(self.dashboard_button)

        self.dashboard_hint = QLabel("Overview of system activity and quick stats")
        self.dashboard_hint.setObjectName("hint")
        self.dashboard_hint.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.dashboard_hint)

        self.employee_button = QPushButton("Manage Employees")
        self.employee_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.employee_button.setObjectName("menuButton")
        self.employee_button.setToolTip("Add, edit, and manage employees (Ctrl+E)")
        card_layout.addWidget(self.employee_button)

        self.employee_hint = QLabel("Create, edit, and organize employee records")
        self.employee_hint.setObjectName("hint")
        self.employee_hint.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.employee_hint)

        self.attendance_button = QPushButton("Mark Attendance")
        self.attendance_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.attendance_button.setObjectName("menuButton")
        self.attendance_button.setToolTip("Start attendance scanning (Ctrl+A)")
        card_layout.addWidget(self.attendance_button)

        self.attendance_hint = QLabel("Record attendance quickly and accurately")
        self.attendance_hint.setObjectName("hint")
        self.attendance_hint.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.attendance_hint)

        self.logout_button = QPushButton("Logout")
        self.logout_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.logout_button.setObjectName("logoutButton")
        card_layout.addWidget(self.logout_button)

        self.logout_hint = QLabel("Sign out and return to the login screen")
        self.logout_hint.setObjectName("hint")
        self.logout_hint.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.logout_hint)

        main_layout.addStretch()
 
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.card)
        h_layout.addStretch()

        main_layout.addLayout(h_layout)

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
            font-size: 30px;
            font-weight: 700;
            color: #f4f7f9;
            letter-spacing: 0.3px;
        }

        QLabel#subtitle {
            font-size: 15px;
            color: #c5cbd0;
            margin-bottom: 6px;
        }

        QLabel#caption {
            font-size: 13px;
            color: #9aa6ac;
            margin-bottom: 14px;
        }

        QLabel#hint {
            font-size: 12px;
            color: #8e9aa1;
            margin-bottom: 10px;
        }

        /* Menu Buttons */
        QPushButton#menuButton {
            background-color: #16c2ff;
            color: #0b1216;
            padding: 14px 18px;
            border-radius: 14px;
            font-size: 16px;
            font-weight: bold;
            min-height: 44px;
        }

        QPushButton#menuButton:hover {
            background-color: #0fb4e6;
        }

        QPushButton#menuButton:pressed {
            background-color: #0a9bc7;
        }

        /* Logout Button */
        QPushButton#logoutButton {
            background-color: #ff4b55;
            color: white;
            padding: 14px 18px;
            border-radius: 14px;
            font-size: 16px;
            font-weight: bold;
            min-height: 44px;
        }

        QPushButton#logoutButton:hover {
            background-color: #e13e47;
        }

        QPushButton#logoutButton:pressed {
            background-color: #c8353d;
        }
        """)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
