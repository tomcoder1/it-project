import tensorflow as tf
import numpy as np
from PIL import Image
from .label import ilabel

interpreter = tf.lite.Interpreter(model_path="model/food101_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB").resize((128, 128))
    img = np.asarray(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def classify_food(image_path):
    input_data = preprocess_image(image_path)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]
    # probs = tf.nn.softmax(output_data).numpy()
    # top_indices = np.argsort(output_data)[::-1][:5]

    # return [(ilabel[idx], probs[idx]) for idx in top_indices]
    top_idx = np.argmax(output_data)
    confidence = output_data[top_idx]

    # label = ilabel[top_idx]
    return ilabel[top_idx]
