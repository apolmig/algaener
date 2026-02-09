#!/usr/bin/env python3
"""
Backend API Server para Voxtral Transcription PWA
Servidor Flask que expone endpoints REST para transcribir audio usando Voxtral
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import tempfile
import logging
from pathlib import Path
import sys

# Agregar el directorio backend al path para importar voxtral_inference
sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Habilitar CORS para todas las rutas

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variable global para almacenar el modelo cargado
voxtral_model = None
MODEL_DIR = os.environ.get('VOXTRAL_MODEL_DIR', 'voxtral-model')

def load_voxtral_model():
    """Carga el modelo Voxtral en memoria (lazy loading)"""
    global voxtral_model
    if voxtral_model is None:
        try:
            logger.info(f"Cargando modelo Voxtral desde {MODEL_DIR}...")
            # Importar aquí para evitar carga al inicio
            import voxtral_inference
            voxtral_model = voxtral_inference.load_model(MODEL_DIR)
            logger.info("Modelo Voxtral cargado exitosamente")
        except Exception as e:
            logger.error(f"Error cargando modelo Voxtral: {e}")
            raise
    return voxtral_model

@app.route('/')
def index():
    """Servir la aplicación PWA"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/health')
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'ok',
        'model_loaded': voxtral_model is not None,
        'model_dir': MODEL_DIR
    })

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    """
    Endpoint principal de transcripción
    Recibe audio y devuelve texto transcrito
    """
    try:
        # Verificar que se envió un archivo
        if 'audio' not in request.files:
            return jsonify({'error': 'No se envió archivo de audio'}), 400

        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'Archivo vacío'}), 400

        # Cargar modelo si no está cargado
        model = load_voxtral_model()

        # Guardar audio temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            audio_file.save(tmp_file.name)
            tmp_path = tmp_file.name

        try:
            # Transcribir usando Voxtral
            logger.info(f"Transcribiendo archivo: {tmp_path}")
            import voxtral_inference

            # Cargar y transcribir
            text = voxtral_inference.transcribe_file(model, tmp_path)

            logger.info(f"Transcripción completada: {len(text)} caracteres")

            return jsonify({
                'success': True,
                'text': text,
                'length': len(text)
            })

        finally:
            # Limpiar archivo temporal
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    except Exception as e:
        logger.error(f"Error en transcripción: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/transcribe-stream', methods=['POST'])
def transcribe_stream():
    """
    Endpoint para transcripción streaming (chunks de audio)
    Para implementación futura de transcripción en tiempo real
    """
    return jsonify({
        'error': 'Streaming no implementado aún'
    }), 501

if __name__ == '__main__':
    # Verificar que existe el directorio del modelo
    if not os.path.exists(MODEL_DIR):
        logger.warning(f"ADVERTENCIA: Directorio del modelo '{MODEL_DIR}' no encontrado")
        logger.warning("Por favor ejecuta: ./download_model.sh en el directorio raíz")

    # Obtener configuración del servidor
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))

    logger.info(f"Iniciando servidor en http://{host}:{port}")
    logger.info(f"PWA disponible en: http://localhost:{port}")

    app.run(host=host, port=port, debug=True)
