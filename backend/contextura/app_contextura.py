import cv2
import mediapipe as mp
import numpy as np
import requests
from flask import Flask, jsonify
from keras.models import load_model
from keras_preprocessing.image import img_to_array

# Cargar el modelo
cnnFingers = load_model('../../models/ModelsPesosTypeFinger/cnn4_modelFingersFinal.h5')
cnnFingers.load_weights('../../models/ModelsPesosTypeFinger/pesos4FingersFinal.h5')

texture_service = Flask(__name__)


def process_image_for_texture(image):
    try:
        color = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Inicializar MediaPipe
        mp_manos = mp.solutions.hands
        manos = mp_manos.Hands(static_image_mode=True)
        resultado = manos.process(color)
        posiciones = []

        if resultado.multi_hand_landmarks:
            for mano in resultado.multi_hand_landmarks:
                for id, lm in enumerate(mano.landmark):
                    alto, ancho, _ = image.shape
                    corx, cory = int(lm.x * ancho), int(lm.y * alto)
                    posiciones.append([id, corx, cory])

            if posiciones:
                # Extraer región de interés (ROI) alrededor del dedo índice
                pto_i5 = posiciones[9]
                x1, y1 = max(0, pto_i5[1] - 80), max(0, pto_i5[2] - 80)
                x2, y2 = x1 + 160, y1 + 160
                dedos_reg = image[y1:y2, x1:x2]
                dedos_reg = cv2.resize(dedos_reg, (200, 200), interpolation=cv2.INTER_CUBIC)

                # Preprocesar la imagen para el modelo
                x_type = cv2.cvtColor(dedos_reg, cv2.COLOR_BGR2GRAY)
                x_type = cv2.GaussianBlur(x_type, (5, 5), 0)
                x_type = cv2.Canny(x_type, 50, 150)
                x_type = np.expand_dims(x_type, axis=-1)
                x_type = np.expand_dims(x_type, axis=0)
                x_type = x_type / 255.0

                # Clasificación del tipo de dedo
                fingers_response = cnnFingers.predict(x_type)

                if fingers_response[0][0] > 0.5:
                    return 'Delgado'
                else:
                    return 'Ancho'
        return 'No se detectaron manos'
    except Exception as e:
        print(f'Error en el procesamiento de la imagen: {e}')
        return 'Error en el procesamiento'


@texture_service.route('/predict-texture', methods=['POST'])
def predict_texture():
    # Obtener la URL de la imagen desde el puerto 5000
    image_url = 'http://localhost:5000/image'  # Cambia esta URL si es diferente

    # Hacer una solicitud GET para obtener la imagen
    response = requests.get(image_url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to retrieve image'}), 500

    # Leer la imagen desde la respuesta
    image = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)

    prediction_result = process_image_for_texture(image)

    if prediction_result:
        return jsonify({'texture_prediction': prediction_result})

    return jsonify({'error': 'No hands detected'}), 400


@texture_service.route('/get-prediction-texture', methods=['GET'])
def get_prediction_texture():
    # Obtener la URL de la imagen desde el puerto 5000
    image_url = 'http://localhost:5000/image'  # Cambia esta URL si es diferente

    # Hacer una solicitud GET para obtener la imagen
    response = requests.get(image_url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to retrieve image'}), 500

    # Leer la imagen desde la respuesta
    image = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)

    prediction_result = process_image_for_texture(image)

    if prediction_result:
        return jsonify({'texture_prediction': prediction_result})

    return jsonify({'error': 'No hands detected'}), 400


if __name__ == '__main__':
    texture_service.run(port=5002)
