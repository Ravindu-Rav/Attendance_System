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
import hashlib


class AdminRegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System — Admin Registration")
        self.setMinimumSize(350, 450)
        self.resize(420, 560)


        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self._build_ui()
        self._apply_styles()
        self._connect_signals()

    def _connect_signals(self):
        """Connect button and link signals"""
        self.register_button.clicked.connect(self._handle_register)
        self.back_label.linkActivated.connect(self._handle_back_to_login)

    def _handle_register(self):
        """Handle register button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        try:
            from app.controllers.auth_controller import register_admin
            register_admin(username, password, confirm_password)
            QMessageBox.information(self, "Success", f"Admin account '{username}' created successfully!")
            self.close()  # Close and return to login
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _handle_back_to_login(self):
        """Handle back to login link click"""
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
        self.title = QLabel("Admin Registration")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        self.subtitle = QLabel("Create the first admin account")
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.subtitle)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setObjectName("input")
        card_layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("input")
        card_layout.addWidget(self.password_input)

        # Confirm Password
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setObjectName("input")
        card_layout.addWidget(self.confirm_password_input)

        # Register Button
        self.register_button = QPushButton("REGISTER ADMIN")
        self.register_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.register_button.setObjectName("registerButton")
        card_layout.addWidget(self.register_button)

        # Back to Login
        back_layout = QHBoxLayout()
        back_layout.addStretch()

        self.back_label = QLabel("<a href='#'>Back to Login</a>")
        self.back_label.setObjectName("link")
        self.back_label.setTextFormat(Qt.RichText)
        self.back_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.back_label.setOpenExternalLinks(False)
        back_layout.addWidget(self.back_label)

        card_layout.addLayout(back_layout)

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.card)
        h_layout.addStretch()

        main_layout.addStretch()
        main_layout.addLayout(h_layout)
        main_layout.addStretch()

    def _apply_styles(self):
        self.setStyleSheet("""
        /* Dark Gradient Background */
        QMainWindow {
            background-color: black;
        }

        QFrame#card {
            background-color: rgba(25, 25, 25, 0.95);
            border-radius: 20px;
            max-width: 420px;
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

        /* Inputs */
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

        /* Register Button */
        QPushButton#registerButton {
            background-color: #00c6ff;
            color: black;
            padding: 12px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
        }

        QPushButton#registerButton:hover {
            background-color: #00a6d6;
        }

        QPushButton#registerButton:pressed {
            background-color: #008bb5;
        }

        /* Link */
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
    import sys
    app = QApplication(sys.argv)
    window = AdminRegistrationWindow()
    window.showMaximized()
    sys.exit(app.exec())