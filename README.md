# 🎙️ VoxTral Transcriptor PWA

Aplicación web progresiva (PWA) para grabar y transcribir audio usando **IA** completamente en local. Sin servicios en la nube, sin costos por uso, 100% privado.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![PyTorch](https://img.shields.io/badge/pytorch-2.0+-orange.svg)

## 🎯 Dos versiones disponibles

### 🌐 [Versión Standalone](STANDALONE.md) - **Recomendada para empezar**
- ✅ **Sin instalación** - Solo abre `standalone.html` en tu navegador
- ✅ **Sin servidor** - Todo funciona en el navegador
- ✅ **WebGPU acelerado** - Usa GPU cuando está disponible
- ✅ **Whisper AI** - Modelos tiny/base/small de OpenAI
- ✅ **Funciona en GitHub Pages** - Despliega gratis en segundos
- 📦 Descarga: 40-250 MB (según modelo)

👉 **[Probar ahora](https://apolmig.github.io/algaener/)** | [Abrir local](standalone.html) | [Guía completa](STANDALONE.md)

### 🚀 Versión Backend (Voxtral) - **Para uso intensivo**
- 🎯 **Máxima precisión** - Voxtral Realtime 4B (este documento)
- ⚡ **Muy rápido** - Optimizado con Metal/BLAS
- 🖥️ **Servidor Flask** - Acceso desde cualquier dispositivo en tu red
- 💾 Descarga: ~9 GB

👉 Continúa leyendo este README para instrucciones

📊 **¿No sabes cuál elegir?** Lee la [comparación detallada](COMPARISON.md)

---

## ✨ Características (Versión Backend)

- 🎤 **Grabación de audio** directamente desde el navegador
- 🤖 **Transcripción con IA** usando Voxtral Realtime 4B
- 📱 **PWA instalable** - funciona como app nativa en móvil
- 🌐 **100% local** - toda la transcripción ocurre en tu máquina
- 🔒 **Privado** - ningún audio sale de tu red local
- 💾 **Historial** - guarda tus transcripciones localmente
- 🎨 **UI moderna** - diseño responsive optimizado para móvil
- ⚡ **Tiempo real** - visualización de forma de onda durante grabación

## 📋 Requisitos

### Sistema
- Python 3.8 o superior
- 16GB RAM mínimo (recomendado 32GB)
- ~10GB espacio en disco para el modelo
- Procesador moderno (recomendado: Apple Silicon M1+ o GPU NVIDIA)

### Software
- Python 3.8+
- pip
- wget o curl (para descargar el modelo)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/apolmig/algaener.git
cd algaener
```

### 2. Ejecutar setup automático

```bash
./setup.sh
```

Este script:
- Crea un entorno virtual de Python
- Instala todas las dependencias
- Descarga el modelo Voxtral (~9GB)
- Configura la aplicación

### 3. Instalación manual (alternativa)

Si prefieres hacerlo manualmente:

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelo
./download_model.sh
```

## 🎯 Uso

### Iniciar el servidor

```bash
# Activar entorno virtual
source venv/bin/activate

# Iniciar servidor backend
python backend/server.py
```

El servidor se iniciará en `http://localhost:5000`

### Acceder desde el navegador

**Desde la misma máquina:**
```
http://localhost:5000
```

**Desde móvil en la misma red WiFi:**
```
http://TU_IP_LOCAL:5000
```

Para encontrar tu IP local:
- **Linux/Mac:** `ifconfig` o `ip addr`
- **Windows:** `ipconfig`

### Usar la aplicación

1. **Verificar estado** - Asegúrate que el servidor está online y el modelo cargado
2. **Dar permisos** - Permite acceso al micrófono cuando se solicite
3. **Grabar** - Presiona el botón "Grabar" y habla
4. **Detener** - Presiona "Detener" cuando termines
5. **Transcribir** - Presiona "Transcribir" para procesar el audio
6. **Resultado** - La transcripción aparecerá en pantalla

### Instalar como PWA

En móvil:
1. Abre la app en el navegador
2. Toca el menú del navegador (⋮)
3. Selecciona "Agregar a pantalla de inicio" o "Instalar app"

En escritorio (Chrome):
1. Busca el icono de instalación (⊕) en la barra de dirección
2. Clic en "Instalar"

## 🏗️ Arquitectura

```
┌─────────────────┐
│  Frontend PWA   │  ← HTML5 + CSS3 + Vanilla JS
│  (Navegador)    │  ← MediaRecorder API
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│  Backend Flask  │  ← API REST
│  (Python)       │  ← Servidor local
└────────┬────────┘
         │
┌────────▼────────┐
│     Voxtral     │  ← Modelo de IA 4B params
│  (PyTorch)      │  ← Transcripción local
└─────────────────┘
```

## 📂 Estructura del proyecto

```
algaener/
├── backend/
│   ├── server.py              # Servidor Flask
│   └── voxtral_inference.py   # Wrapper de Voxtral
├── frontend/
│   ├── index.html             # UI principal
│   ├── css/
│   │   └── style.css          # Estilos
│   ├── js/
│   │   └── app.js             # Lógica frontend
│   ├── manifest.json          # Configuración PWA
│   ├── sw.js                  # Service Worker
│   └── icon.svg               # Icono de la app
├── voxtral-model/             # Modelo descargado (9GB)
│   ├── consolidated.safetensors
│   ├── tekken.json
│   └── params.json
├── requirements.txt           # Dependencias Python
├── setup.sh                   # Script de instalación
├── download_model.sh          # Script descarga modelo
└── README.md                  # Este archivo
```

## 🔧 Configuración

### Variables de entorno

```bash
# Puerto del servidor (default: 5000)
export PORT=5000

# Host (default: 0.0.0.0 para acceso remoto)
export HOST=0.0.0.0

# Directorio del modelo (default: voxtral-model)
export VOXTRAL_MODEL_DIR=voxtral-model
```

## 📱 Compatibilidad

### Navegadores soportados

| Navegador | Desktop | Móvil | Grabación | PWA |
|-----------|---------|-------|-----------|-----|
| Chrome    | ✅      | ✅    | ✅        | ✅  |
| Safari    | ✅      | ✅    | ✅        | ✅  |
| Firefox   | ✅      | ✅    | ✅        | ⚠️  |
| Edge      | ✅      | ✅    | ✅        | ✅  |

⚠️ = Soporte limitado

### Sistemas operativos

- ✅ macOS (Apple Silicon recomendado)
- ✅ Linux (Ubuntu, Debian, Fedora)
- ⚠️ Windows (soporte experimental)
- ✅ iOS (Safari)
- ✅ Android (Chrome)

## 🙏 Créditos

- **Voxtral** - [antirez/voxtral.c](https://github.com/antirez/voxtral.c)
- **Mistral AI** - [Voxtral Realtime 4B](https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. El modelo Voxtral está licenciado bajo Apache-2.0 por Mistral AI.

---

Hecho con ❤️ usando [Voxtral](https://github.com/antirez/voxtral.c)
