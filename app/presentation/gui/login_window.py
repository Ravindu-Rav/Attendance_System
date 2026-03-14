from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QMessageBox,
)
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.database.db import get_connection


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System — Login")
        self.setMinimumSize(420, 560)
        self.resize(420, 560)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self._build_ui()
        self._apply_styles()
        self._connect_signals()

    def _connect_signals(self):
        self.login_button.clicked.connect(self._handle_login)

    def _handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both username and password.")
            return

        import hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM Admin WHERE username = ? AND password = ?", (username, hashed_password))
            admin = c.fetchone()
            conn.close()

            if admin:
                QMessageBox.information(self, "Login Successful", "Welcome to the Attendance System!")
                self._open_main_window()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password. Please try again.")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to authenticate: {str(e)}")

    def _open_main_window(self):
        from .main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def _handle_register_admin(self):
        from .admin_registration_window import AdminRegistrationWindow
        self.register_window = AdminRegistrationWindow()
        self.register_window.show()
        self.hide()

    def _build_ui(self):
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.card = QFrame()
        self.card.setObjectName("card")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 50, 40, 40)
        card_layout.setSpacing(25)

        self.title = QLabel("Attendance System")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        self.subtitle = QLabel("Welcome back! Please login")
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.subtitle)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or Email")
        self.username_input.setObjectName("input")
        card_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("input")
        card_layout.addWidget(self.password_input)

        self.login_button = QPushButton("LOGIN")
        self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_button.setObjectName("loginButton")
        card_layout.addWidget(self.login_button)

        # Create account link (only if admin doesn't exist)
        if not self._admin_exists():
            register_layout = QHBoxLayout()
            register_layout.setAlignment(Qt.AlignCenter)

            self.register_label = QLabel(
                "Don't have an account? <a href='#'>Create one</a>"
            )
            self.register_label.setObjectName("registerLink")
            self.register_label.setTextFormat(Qt.RichText)
            self.register_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            self.register_label.setOpenExternalLinks(False)
            self.register_label.linkActivated.connect(self._handle_register_admin)

            register_layout.addWidget(self.register_label)
            card_layout.addLayout(register_layout)

        forgot_layout = QHBoxLayout()
        forgot_layout.addStretch()

        self.forgot_label = QLabel("<a href='#'>Forgot Password?</a>")
        self.forgot_label.setObjectName("link")
        self.forgot_label.setTextFormat(Qt.RichText)
        self.forgot_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.forgot_label.setOpenExternalLinks(False)
        forgot_layout.addWidget(self.forgot_label)

        card_layout.addLayout(forgot_layout)

        main_layout.addStretch()
        main_layout.addWidget(self.card)
        main_layout.addStretch()

    def _admin_exists(self):
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM Admin")
            count = c.fetchone()[0]
            conn.close()
            return count > 0
        except:
            return False

    def _apply_styles(self):
        self.setStyleSheet("""
        QMainWindow {
            background: qlineargradient(
                spread:pad,
                x1:0, y1:0,
                x2:1, y2:1,
                stop:0 #0f2027,
                stop:1 #203a43
            );
        }

        QFrame#card {
            background-color: rgba(25, 25, 25, 0.95);
            border-radius: 20px;
        }

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

        QLineEdit#input {
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #444;
            font-size: 14px;
            background-color: #2b2b2b;
            color: white;
        }

        QLineEdit#input:focus {
            border: 2px solid #00c6ff;
            background-color: #333;
        }

        QPushButton#loginButton {
            background-color: #00c6ff;
            color: black;
            padding: 12px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
        }

        QPushButton#loginButton:hover {
            background-color: #00a6d6;
        }

        QPushButton#loginButton:pressed {
            background-color: #008bb5;
        }

        QLabel#registerLink {
            font-size: 13px;
            color: #bbbbbb;
        }

        QLabel#registerLink a {
            color: #00c6ff;
            text-decoration: none;
            font-weight: bold;
        }

        QLabel#registerLink a:hover {
            text-decoration: underline;
        }

        QLabel#link {
            font-size: 13px;
        }

        QLabel#link a {
            color: #00c6ff;
            text-decoration: none;
        }

        QLabel#link a:hover {
            text-decoration: underline;
        }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())