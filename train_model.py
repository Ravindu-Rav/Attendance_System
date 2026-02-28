import cv2
import os
import numpy as np

dataset_path = "dataset"


def get_images_and_labels(path):

    face_samples = []
    ids = []

    for employee_id in os.listdir(path):

        employee_folder = os.path.join(path, employee_id)

        for image_name in os.listdir(employee_folder):

            image_path = os.path.join(employee_folder, image_name)

            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            face_samples.append(img)
            ids.append(int(employee_id))

    return face_samples, ids


print("Training faces...")

faces, ids = get_images_and_labels(dataset_path)

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.train(faces, np.array(ids))

recognizer.save("trainer.yml")

print("Training complete. Model saved as trainer.yml")