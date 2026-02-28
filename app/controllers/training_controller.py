"""Training Controller"""
from app.services.training_service import train_model
from app.config.settings import DATASET_DIR, MODEL_PATH


def handle_train_model():
    """Handle model training workflow"""
    try:
        success = train_model(DATASET_DIR, MODEL_PATH)
        if success:
            print("Model training completed successfully")
        else:
            print("Model training failed")
    except Exception as e:
        print(f"Error during model training: {e}")
