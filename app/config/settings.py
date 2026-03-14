# Database Configuration
DATABASE_NAME = "attendance.db"
DATABASE_PATH = f"sqlite:///{DATABASE_NAME}"

# Dataset and Model Configuration
DATASET_DIR = "dataset"
MODEL_PATH = "models_storage/trainer.yml"

# Face Recognition Settings
FACE_RECOGNITION_CONFIDENCE_THRESHOLD = 60
DEFAULT_CAPTURE_SAMPLES = 50
FACE_DETECTOR_MODEL = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Camera Settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Training Settings
TRAINING_TEST_SIZE = 0.2
TRAINING_RANDOM_STATE = 42

# UI Configuration
WINDOW_DEFAULT_WIDTH = 420
WINDOW_DEFAULT_HEIGHT = 560
WINDOW_MIN_WIDTH = 350
WINDOW_MIN_HEIGHT = 450

# Application Settings
APP_NAME = "Attendance System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "app.log"

# Security Settings
PASSWORD_MIN_LENGTH = 6
SESSION_TIMEOUT_MINUTES = 30

# Default Values
DEFAULT_EMPLOYEE_AGE = 25
DEFAULT_EMPLOYEE_GENDER = 1  # 1=Male, 2=Female
DEFAULT_PASSWORD = "password123"