#!/bin/bash
# Script para descargar el modelo Voxtral desde HuggingFace

set -e

MODEL_DIR="voxtral-model"
HF_REPO="mistralai/Voxtral-Mini-4B-Realtime-2602"
BASE_URL="https://huggingface.co/${HF_REPO}/resolve/main"

echo "Descargando modelo Voxtral desde HuggingFace..."
echo "Repositorio: ${HF_REPO}"
echo ""

# Crear directorio del modelo
mkdir -p "${MODEL_DIR}"

# Función para descargar con barra de progreso
download_file() {
    local filename=$1
    local url="${BASE_URL}/${filename}"
    local output="${MODEL_DIR}/${filename}"

    if [ -f "${output}" ]; then
        echo "✓ ${filename} ya existe, omitiendo..."
        return
    fi

    echo "Descargando ${filename}..."
    if command -v wget &> /dev/null; then
        wget --continue --progress=bar:force -O "${output}" "${url}"
    elif command -v curl &> /dev/null; then
        curl -L --progress-bar -C - -o "${output}" "${url}"
    else
        echo "ERROR: Se requiere wget o curl para descargar"
        exit 1
    fi
    echo "✓ ${filename} descargado"
    echo ""
}

# Descargar archivos del modelo
echo "Iniciando descargas..."
echo ""

# Archivo principal de pesos (~8.9 GB)
download_file "consolidated.safetensors"

# Tokenizer
download_file "tekken.json"

# Configuración del modelo
download_file "params.json"

echo ""
echo "================================"
echo "Descarga completada exitosamente!"
echo "================================"
echo ""
echo "Archivos descargados en: ${MODEL_DIR}/"
ls -lh "${MODEL_DIR}/"
echo ""
