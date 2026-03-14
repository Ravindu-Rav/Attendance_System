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
)
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System — Login")
        self.setFixedSize(420, 560)

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
        self.title = QLabel("Attendance System")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        self.subtitle = QLabel("Welcome back! Please login")
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.subtitle)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or Email")
        self.username_input.setObjectName("input")
        card_layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("input")
        card_layout.addWidget(self.password_input)

        # Login Button
        self.login_button = QPushButton("LOGIN")
        self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_button.setObjectName("loginButton")
        card_layout.addWidget(self.login_button)

        # Forgot password
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

        /* Login Button */
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
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())