import cv2
import os

model_path = os.path.join('models_storage', 'trainer.yml')
print('model exists', os.path.exists(model_path), 'size', os.path.getsize(model_path) if os.path.exists(model_path) else None)

rec = cv2.face.LBPHFaceRecognizer_create()
try:
    rec.read(model_path)
    print('loaded model')
except Exception as e:
    print('load error', e)

img_path = os.path.join('dataset', '1', '1.jpg')
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
print('img exists', os.path.exists(img_path), 'shape', None if img is None else img.shape)

try:
    id, pred = rec.predict(img)
    print('predict', id, pred)
except Exception as e:
    print('predict error', e)
