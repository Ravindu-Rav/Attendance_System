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
    QProgressBar,
    QTextEdit,
)
from PySide6.QtGui import QColor, QCursor
from PySide6.QtCore import Qt, QThread, Signal
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.controllers.training_controller import handle_train_model


class TrainingThread(QThread):
    """Thread for training model to avoid blocking UI"""
    progress = Signal(str)
    finished = Signal(bool, str)

    def run(self):
        """Run training in thread"""
        try:
            # Redirect stdout to capture training output
            import io
            from contextlib import redirect_stdout
            
            f = io.StringIO()
            with redirect_stdout(f):
                result = handle_train_model()
            
            output = f.getvalue()
            self.progress.emit(output)
            self.finished.emit(True, "Training completed successfully!")
        except Exception as e:
            self.finished.emit(False, str(e))


class TrainingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System — Train Model")
        self.setMinimumSize(600, 500)
        self.resize(600, 500)

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
        self.title = QLabel("Train Recognition Model")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title)

        self.subtitle = QLabel("Train the face recognition model with employee photos")
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.subtitle)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setVisible(False)
        card_layout.addWidget(self.progress_bar)

        # Output Text Area
        self.output_text = QTextEdit()
        self.output_text.setObjectName("outputText")
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(200)
        card_layout.addWidget(self.output_text)

        # Train Button
        self.train_button = QPushButton("Start Training")
        self.train_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.train_button.setObjectName("trainButton")
        self.train_button.clicked.connect(self._start_training)
        card_layout.addWidget(self.train_button)

        # Back Button
        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self._back_to_main)
        card_layout.addWidget(self.back_button)

        main_layout.addStretch()
        main_layout.addWidget(self.card)
        main_layout.addStretch()

    def _start_training(self):
        """Start the training process"""
        self.train_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.output_text.clear()
        self.output_text.append("Starting training...\n")

        self.training_thread = TrainingThread()
        self.training_thread.progress.connect(self._update_progress)
        self.training_thread.finished.connect(self._training_finished)
        self.training_thread.start()

    def _update_progress(self, text):
        """Update progress text"""
        self.output_text.append(text)

    def _training_finished(self, success, message):
        """Handle training completion"""
        self.progress_bar.setVisible(False)
        self.train_button.setEnabled(True)
        if success:
            self.output_text.append(f"\n✅ {message}")
        else:
            self.output_text.append(f"\n❌ Training failed: {message}")

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

        QLabel#subtitle {
            font-size: 14px;
            color: #bbbbbb;
            margin-bottom: 10px;
        }

        /* Progress Bar */
        QProgressBar#progressBar {
            border: 2px solid #444;
            border-radius: 5px;
            text-align: center;
        }

        QProgressBar#progressBar::chunk {
            background-color: #00c6ff;
        }

        /* Output Text */
        QTextEdit#outputText {
            background-color: #2b2b2b;
            border-radius: 10px;
            padding: 10px;
            color: white;
            font-family: monospace;
            font-size: 12px;
        }

        /* Train Button */
        QPushButton#trainButton {
            background-color: #00c6ff;
            color: black;
            padding: 15px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
        }

        QPushButton#trainButton:hover {
            background-color: #00a6d6;
        }

        QPushButton#trainButton:pressed {
            background-color: #008bb5;
        }

        QPushButton#trainButton:disabled {
            background-color: #666;
            color: #ccc;
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
    window = TrainingWindow()
    window.show()
    sys.exit(app.exec())