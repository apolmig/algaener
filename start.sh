#!/bin/bash
# Script de inicio para Voxtral PWA

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================="
echo "  VoxTral PWA - Servidor"
echo -e "==================================${NC}"
echo ""

# Verificar si estamos en el directorio correcto
if [ ! -f "backend/server.py" ]; then
    echo -e "${RED}ERROR: Ejecuta este script desde el directorio raíz del proyecto${NC}"
    exit 1
fi

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Entorno virtual no encontrado${NC}"
    echo "Ejecuta primero: ./setup.sh"
    exit 1
fi

# Activar entorno virtual
echo -e "${GREEN}→${NC} Activando entorno virtual..."
source venv/bin/activate

# Verificar que el modelo existe
if [ ! -d "voxtral-model" ] || [ ! -f "voxtral-model/consolidated.safetensors" ]; then
    echo -e "${YELLOW}⚠️  Modelo Voxtral no encontrado${NC}"
    echo ""
    echo "Necesitas descargar el modelo primero (~9GB)."
    echo "¿Descargar ahora? (s/n)"
    read -r response
    if [[ "$response" =~ ^([sS][iI]|[sS])$ ]]; then
        ./download_model.sh
    else
        echo ""
        echo "Para descargar más tarde: ./download_model.sh"
        echo "O usa la versión standalone: open standalone.html"
        exit 1
    fi
fi

# Obtener IP local
if command -v hostname &> /dev/null; then
    LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "unknown")
else
    LOCAL_IP="unknown"
fi

# Puerto
PORT=${PORT:-5000}

echo ""
echo -e "${GREEN}→${NC} Iniciando servidor Flask..."
echo ""
echo -e "${GREEN}=================================="
echo "  Servidor listo"
echo -e "==================================${NC}"
echo ""
echo "Accede desde:"
echo -e "  ${GREEN}Local:${NC}  http://localhost:${PORT}"

if [ "$LOCAL_IP" != "unknown" ]; then
    echo -e "  ${GREEN}Red:${NC}    http://${LOCAL_IP}:${PORT}"
fi

echo ""
echo "Presiona Ctrl+C para detener"
echo ""

# Iniciar servidor
python backend/server.py
