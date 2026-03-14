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
    QListWidget,
    QListWidgetItem,
)
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt


class EmployeeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System — Manage Employees")
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
        self.title = QLabel("Manage Employees")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        # Employee List
        self.employee_list = QListWidget()
        self.employee_list.setObjectName("employeeList")
        # Placeholder items
        self.employee_list.addItem("John Doe - ID: 001")
        self.employee_list.addItem("Jane Smith - ID: 002")
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
        from main_window import MainWindow
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

        /* Employee List */
        QListWidget#employeeList {
            background-color: #2b2b2b;
            border-radius: 10px;
            padding: 10px;
            color: white;
            font-size: 14px;
        }

        QListWidget#employeeList::item {
            padding: 5px;
            border-bottom: 1px solid #444;
        }

        QListWidget#employeeList::item:selected {
            background-color: #00c6ff;
            color: black;
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

        /* Buttons */
        QPushButton#addButton {
            background-color: #00c6ff;
            color: black;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
        }

        QPushButton#addButton:hover {
            background-color: #00a6d6;
        }

        QPushButton#editButton {
            background-color: #ffa500;
            color: black;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
        }

        QPushButton#editButton:hover {
            background-color: #e69500;
        }

        QPushButton#deleteButton {
            background-color: #ff4444;
            color: white;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
        }

        QPushButton#deleteButton:hover {
            background-color: #cc3333;
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
    window = EmployeeWindow()
    window.show()
    sys.exit(app.exec())
