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
import subprocess

# Agregar el directorio backend al path para importar voxtral_inference
sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Habilitar CORS para todas las rutas

# Configuración de logging mejorada
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Formatos de audio soportados
ALLOWED_AUDIO_FORMATS = {
    'audio/wav', 'audio/x-wav', 'audio/wave',
    'audio/webm', 'audio/ogg', 'audio/mpeg',
    'audio/mp4', 'audio/m4a', 'audio/x-m4a'
}

# Límite de tamaño de archivo (50 MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

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

def convert_to_wav(input_path, output_path):
    """
    Convierte un archivo de audio a formato WAV 16kHz mono usando ffmpeg
    """
    try:
        # Verificar si ffmpeg está disponible
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("ffmpeg no disponible, intentando usar archivo directamente")
        return input_path

    try:
        # Convertir a WAV 16kHz mono
        command = [
            'ffmpeg', '-y', '-i', input_path,
            '-ar', '16000',  # Sample rate 16kHz
            '-ac', '1',       # Mono
            '-c:a', 'pcm_s16le',  # 16-bit PCM
            output_path
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        logger.info(f"Audio convertido exitosamente a WAV: {output_path}")
        return output_path

    except subprocess.CalledProcessError as e:
        logger.error(f"Error convirtiendo audio: {e.stderr}")
        raise Exception(f"Error al convertir audio: {e.stderr}")

def validate_audio_file(audio_file):
    """Valida que el archivo de audio sea válido"""
    # Verificar tamaño
    audio_file.seek(0, os.SEEK_END)
    file_size = audio_file.tell()
    audio_file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return False, f"Archivo demasiado grande ({file_size / 1024 / 1024:.1f} MB). Máximo: 50 MB"

    if file_size == 0:
        return False, "Archivo vacío"

    # Verificar tipo MIME
    content_type = audio_file.content_type
    if content_type not in ALLOWED_AUDIO_FORMATS:
        logger.warning(f"Tipo de audio no reconocido: {content_type}, intentando procesar de todos modos")

    return True, None

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
    tmp_input_path = None
    tmp_wav_path = None

    try:
        # Verificar que se envió un archivo
        if 'audio' not in request.files:
            return jsonify({'error': 'No se envió archivo de audio'}), 400

        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'Archivo vacío'}), 400

        # Validar archivo
        is_valid, error_msg = validate_audio_file(audio_file)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        logger.info(f"Recibido archivo: {audio_file.filename}, tipo: {audio_file.content_type}")

        # Cargar modelo si no está cargado
        try:
            model = load_voxtral_model()
        except Exception as e:
            return jsonify({
                'error': 'Error al cargar el modelo',
                'details': str(e)
            }), 500

        # Guardar audio temporalmente
        file_ext = os.path.splitext(audio_file.filename)[1] or '.webm'
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            audio_file.save(tmp_file.name)
            tmp_input_path = tmp_file.name

        # Convertir a WAV si es necesario
        if not tmp_input_path.endswith('.wav'):
            tmp_wav_path = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
            try:
                convert_to_wav(tmp_input_path, tmp_wav_path)
                transcribe_path = tmp_wav_path
            except Exception as e:
                logger.warning(f"No se pudo convertir audio, usando original: {e}")
                transcribe_path = tmp_input_path
        else:
            transcribe_path = tmp_input_path

        # Transcribir usando Voxtral
        logger.info(f"Transcribiendo archivo: {transcribe_path}")
        import voxtral_inference

        try:
            text = voxtral_inference.transcribe_file(model, transcribe_path)
        except Exception as e:
            logger.error(f"Error en transcripción Voxtral: {e}", exc_info=True)
            return jsonify({
                'error': 'Error al transcribir audio',
                'details': str(e)
            }), 500

        logger.info(f"Transcripción completada: {len(text)} caracteres")

        return jsonify({
            'success': True,
            'text': text,
            'length': len(text),
            'filename': audio_file.filename
        })

    except Exception as e:
        logger.error(f"Error general en transcripción: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'details': str(e)
        }), 500

    finally:
        # Limpiar archivos temporales
        for path in [tmp_input_path, tmp_wav_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    logger.warning(f"No se pudo eliminar archivo temporal {path}: {e}")

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
