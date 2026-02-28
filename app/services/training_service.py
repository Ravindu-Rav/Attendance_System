"""Model Training Service"""
import cv2
import os
import numpy as np
from app.config.settings import DATASET_DIR, MODEL_PATH


def get_images_and_labels(path):
    """Get images and labels from dataset directory
    
    Args:
        path: Path to dataset directory
    
    Returns:
        Tuple of (face_samples, ids)
    """
    face_samples = []
    ids = []

    if not os.path.exists(path):
        print(f"Dataset directory not found: {path}")
        return face_samples, ids

    for employee_id in os.listdir(path):
        employee_folder = os.path.join(path, employee_id)

        if not os.path.isdir(employee_folder):
            continue

        for image_name in os.listdir(employee_folder):
            image_path = os.path.join(employee_folder, image_name)

            try:
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    face_samples.append(img)
                    ids.append(int(employee_id))
            except Exception as e:
                print(f"Error reading {image_path}: {e}")

    return face_samples, ids


def train_model(dataset_path=DATASET_DIR, model_path=MODEL_PATH):
    """Train face recognizer model
    
    Args:
        dataset_path: Path to dataset directory
        model_path: Path to save trained model
    
    Returns:
        True if training successful, False otherwise
    """
    print("Loading training data...")
    faces, ids = get_images_and_labels(dataset_path)

    if len(faces) == 0:
        print("No training data found!")
        return False

    print(f"Training model with {len(faces)} images from {len(set(ids))} employees...")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(ids))

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    recognizer.save(model_path)

    print(f"Training complete. Model saved as {model_path}")
    return True
