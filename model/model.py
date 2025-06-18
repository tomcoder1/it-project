import onnxruntime as ort
import numpy as np
from PIL import Image
from .label import ilabel
import os

model_path = os.path.join(os.path.dirname(__file__), "food101.onnx")
session = ort.InferenceSession(model_path)

def preprocess_image(path):
    img = Image.open(path).convert("RGB").resize((224, 224))
    img = np.array(img).astype(np.float32) / 255.0 
    img = img.transpose(2, 0, 1)
    img = np.expand_dims(img, 0)
    return img

def classify_food(path):
    try:
        input_tensor = preprocess_image(path)
        outputs = session.run(None, {"pixel_values": input_tensor})
        logits = outputs[0]
        probs = softmax(logits)
        top_index = np.argmax(probs)

        return ilabel[top_index]
    except Exception as e:
        print(f"Error during ONNX inference: {e}")
        return None

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=1, keepdims=True)