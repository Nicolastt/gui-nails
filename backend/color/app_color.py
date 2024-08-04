import cv2
import mediapipe as mp
import numpy as np
import requests
from flask import Flask, jsonify
from keras.models import load_model
from keras_preprocessing.image import img_to_array

# Cargar el modelo
cnnHands = load_model('../../models/ModelsPesosHandsColor/cnn_modelHandsFinal.h5')
cnnHands.load_weights('../../models/ModelsPesosHandsColor/pesosHandsFinal.h5')


# Inicializar MediaPipe una vez
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True)
drawing = mp.solutions.drawing_utils

# Crear la aplicación Flask
color = Flask(__name__)

def process_image(image):
    color = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Procesar la imagen para detectar manos
    result = hands.process(color)
    positions = []

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                height, width, _ = image.shape
                pos_x, pos_y = int(lm.x * width), int(lm.y * height)
                positions.append([id, pos_x, pos_y])
            drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if positions:
            # Tomar la región de interés (ROI) alrededor de la palma de la mano
            point_index5 = positions[9]
            x1, y1 = max(0, point_index5[1] - 80), max(0, point_index5[2] - 80)
            x2, y2 = x1 + 160, y1 + 160
            hand_region = image[y1:y2, x1:x2]
            hand_region = cv2.resize(hand_region, (200, 200), interpolation=cv2.INTER_CUBIC)

            # Clasificación del color de piel
            x = img_to_array(hand_region)
            x = np.expand_dims(x, axis=0)
            x = x / 255.0

            color_prediction = cnnHands.predict(x)
            prediction_result = "Morocho" if color_prediction[0][0] > 0.5 else "Blanco"

            return prediction_result

    return None

def get_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
        return image
    else:
        return None

def handle_prediction(image_url):
    image = get_image_from_url(image_url)
    if image is None:
        return jsonify({'error': 'Failed to retrieve image'}), 500

    prediction_result = process_image(image)
    if prediction_result:
        return jsonify({'prediction': prediction_result})
    else:
        return jsonify({'error': 'No hands detected'}), 400

@color.route('/predict-color', methods=['POST'])
def predict_color():
    image_url = 'http://localhost:5000/image'
    return handle_prediction(image_url)

@color.route('/get-prediction-color', methods=['GET'])
def get_prediction_color():
    image_url = 'http://localhost:5000/image'
    return handle_prediction(image_url)

if __name__ == '__main__':
    color.run(port=5001)
