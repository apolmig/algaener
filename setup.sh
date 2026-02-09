#!/bin/bash
# Setup script para Voxtral PWA

set -e

echo "=================================="
echo "  Voxtral PWA - Setup Script"
echo "=================================="
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar Python
echo -e "${YELLOW}[1/5]${NC} Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 no está instalado${NC}"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION encontrado"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}ERROR: pip3 no está instalado${NC}"
    exit 1
fi

# Crear entorno virtual
echo ""
echo -e "${YELLOW}[2/5]${NC} Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Entorno virtual creado"
else
    echo -e "${GREEN}✓${NC} Entorno virtual ya existe"
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
echo ""
echo -e "${YELLOW}[3/5]${NC} Instalando dependencias..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

echo -e "${GREEN}✓${NC} Dependencias instaladas"

# Descargar modelo Voxtral
echo ""
echo -e "${YELLOW}[4/5]${NC} Descargando modelo Voxtral..."
if [ ! -d "voxtral-model" ]; then
    echo "Este paso descargará ~9GB de datos. ¿Continuar? (s/n)"
    read -r response
    if [[ "$response" =~ ^([sS][iI]|[sS])$ ]]; then
        ./download_model.sh
        echo -e "${GREEN}✓${NC} Modelo descargado"
    else
        echo -e "${YELLOW}!${NC} Modelo NO descargado. Ejecuta './download_model.sh' más tarde"
    fi
else
    echo -e "${GREEN}✓${NC} Modelo ya existe"
fi

# Generar iconos (opcional)
echo ""
echo -e "${YELLOW}[5/5]${NC} Configurando iconos PWA..."
if command -v convert &> /dev/null; then
    # Si ImageMagick está instalado, generar PNGs desde SVG
    convert -background none -resize 192x192 frontend/icon.svg frontend/icon-192.png 2>/dev/null || true
    convert -background none -resize 512x512 frontend/icon.svg frontend/icon-512.png 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Iconos generados"
else
    echo -e "${YELLOW}!${NC} ImageMagick no encontrado. Los iconos deben generarse manualmente"
    echo "   Puedes instalar ImageMagick con: sudo apt install imagemagick (Ubuntu/Debian)"
fi

echo ""
echo -e "${GREEN}=================================="
echo "  Setup completado exitosamente!"
echo "==================================${NC}"
echo ""
echo "Para iniciar la aplicación:"
echo "  1. Activa el entorno virtual: source venv/bin/activate"
echo "  2. Ejecuta el servidor: python backend/server.py"
echo "  3. Abre http://localhost:5000 en tu navegador"
echo ""
echo "Desde un móvil en la misma red:"
echo "  Abre http://TU_IP_LOCAL:5000"
echo ""
