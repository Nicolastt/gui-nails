import os
import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '../../frontend/src/images'
BASE_IMAGE_DIR = 'static/images'

# Asegurar que la carpeta de subida de imágenes exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Definir posibles combinaciones de predicciones y sus respectivas carpetas
possible_combinations = {
    ('Morocho', 'Delgado'): 'Morocho-Delgado',
    ('Morocho', 'Ancho'): 'Morocho-Ancho',
    ('Blanco', 'Delgado'): 'Blanco-Delgado',
    ('Blanco', 'Ancho'): 'Blanco-Ancho'
}

# Variable global para almacenar las predicciones
predictions_cache = {}

def get_prediction_from_service(service_url):
    try:
        response = requests.get(service_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request to {service_url} failed: {str(e)}")

@app.route('/process-image', methods=['POST'])
def process_image():
    global predictions_cache

    try:
        image = request.files['image']
        file_path = os.path.join(UPLOAD_FOLDER, 'uploaded_image.jpg')

        # Guardar la imagen en el servidor
        image.save(file_path)

        # Obtener las predicciones de color y textura
        color_prediction = get_prediction_from_service('http://127.0.0.1:5001/get-prediction-color').get('prediction')
        texture_prediction = get_prediction_from_service('http://127.0.0.1:5002/get-prediction-texture').get('texture_prediction')

        # Cachear las predicciones
        predictions_cache['color'] = color_prediction
        predictions_cache['texture'] = texture_prediction

        # Combinar predicciones y obtener la carpeta de imágenes correspondiente
        combination_key = (color_prediction, texture_prediction)
        folder_name = possible_combinations.get(combination_key, 'default')

        return jsonify({
            'result': f"{color_prediction}-{texture_prediction}",
            'recommendation': folder_name
        })

    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/image', methods=['GET'])
def get_image():
    file_path = os.path.join(UPLOAD_FOLDER, 'uploaded_image.jpg')
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/jpeg')
    else:
        return jsonify({'error': 'Image not found'}), 404

@app.route('/images/<folder_name>', methods=['GET'])
def get_images(folder_name):
    try:
        # Construir la ruta completa de la carpeta de imágenes
        folder_path = os.path.join(BASE_IMAGE_DIR, folder_name)

        # Verificar si el directorio existe
        if not os.path.isdir(folder_path):
            return jsonify({'error': 'Directory not found'}), 404

        # Filtrar solo los archivos de imagen
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

        return jsonify({'images': image_files})

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    try:
        # Verificar si hay predicciones almacenadas
        if 'color' not in predictions_cache or 'texture' not in predictions_cache:
            return jsonify({'error': 'No predictions available'}), 400

        # Acceder a las predicciones almacenadas
        color = predictions_cache['color']
        contextura = predictions_cache['texture']

        # Crear una combinación en formato a-b
        combination_key = (color, contextura)

        # Obtener la carpeta de imágenes basada en la combinación de predicciones
        folder_name = possible_combinations.get(combination_key, 'default')

        return jsonify({
            'recommendation': folder_name
        })

    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000)
