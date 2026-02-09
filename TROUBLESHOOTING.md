# 🔧 Guía de Troubleshooting

Soluciones a los problemas más comunes en VoxTral PWA.

## 📑 Índice rápido

- [Instalación](#instalación)
- [Modelo no carga](#modelo-no-carga)
- [Servidor](#servidor)
- [Audio](#audio)
- [Transcripción](#transcripción)
- [Red/Conectividad](#redconectividad)
- [Rendimiento](#rendimiento)

---

## Instalación

### ❌ Error: `pip install` falla

**Síntomas:**
```
ERROR: Could not install packages due to an OSError
```

**Soluciones:**

1. **Actualiza pip:**
```bash
pip install --upgrade pip
```

2. **Usa Python 3.8+:**
```bash
python3 --version  # Debe ser 3.8 o superior
```

3. **Instala paquetes del sistema (Linux):**
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev libsndfile1

# Fedora
sudo dnf install python3-devel libsndfile

# macOS (con Homebrew)
brew install libsndfile
```

### ❌ Error: `./setup.sh` no ejecuta

**Solución:**
```bash
chmod +x setup.sh
./setup.sh
```

---

## Modelo no carga

### ❌ Error: "Modelo no encontrado"

**Verificar que el modelo existe:**
```bash
ls -lh voxtral-model/
# Debe mostrar:
# - consolidated.safetensors (~8.9 GB)
# - tekken.json (~15 MB)
# - params.json (~1 KB)
```

**Si falta algún archivo:**
```bash
./download_model.sh
```

### ❌ Error: "Out of memory" al cargar modelo

**Síntomas:**
```
RuntimeError: [enforce fail at alloc_cpu.cpp:79]
```

**Causas:**
- RAM insuficiente (< 16 GB)

**Soluciones:**

1. **Cerrar aplicaciones:**
```bash
# macOS
Activity Monitor → Cerrar apps pesadas

# Linux
htop → Matar procesos pesados
```

2. **Usar versión standalone:**
```bash
open standalone.html  # No necesita 9GB de modelo
```

3. **Aumentar swap (Linux):**
```bash
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### ❌ Error: Descarga del modelo se interrumpe

**Síntomas:**
```
curl: (56) Recv failure: Connection reset by peer
```

**Soluciones:**

1. **Descargar con curl/wget directamente:**
```bash
cd voxtral-model

# Descargar pesos principales
wget https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602/resolve/main/consolidated.safetensors

# Descargar tokenizer
wget https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602/resolve/main/tekken.json

# Descargar configuración
wget https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602/resolve/main/params.json
```

2. **Usar `--continue` para reanudar:**
```bash
wget --continue https://huggingface.co/...
```

---

## Servidor

### ❌ Error: "Address already in use"

**Síntomas:**
```
OSError: [Errno 48] Address already in use
```

**Causas:**
- Puerto 5000 ocupado por otra aplicación

**Soluciones:**

1. **Usar otro puerto:**
```bash
PORT=8000 python backend/server.py
```

2. **Matar proceso en puerto 5000:**
```bash
# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

3. **Encontrar qué usa el puerto:**
```bash
lsof -i :5000
```

### ❌ Error: "No module named 'flask'"

**Síntomas:**
```
ModuleNotFoundError: No module named 'flask'
```

**Causa:**
- Entorno virtual no activado

**Solución:**
```bash
source venv/bin/activate
# Debe aparecer (venv) en el prompt
```

### ❌ Error: "ImportError: libsndfile.so.1"

**Síntomas (Linux):**
```
OSError: cannot load library 'libsndfile.so.1'
```

**Solución:**
```bash
# Ubuntu/Debian
sudo apt-get install libsndfile1

# Fedora
sudo dnf install libsndfile

# Arch
sudo pacman -S libsndfile
```

---

## Audio

### ❌ Error: "No se puede acceder al micrófono"

**Síntomas:**
- Botón "Grabar" no funciona
- Error: `NotAllowedError: Permission denied`

**Soluciones:**

1. **Verificar permisos del navegador:**

**Chrome:**
```
chrome://settings/content/microphone
→ Verificar que el sitio tiene permiso
```

**Firefox:**
```
about:preferences#privacy
→ Permisos → Micrófono
```

**Safari:**
```
Preferencias → Sitios web → Micrófono
```

2. **Usar HTTPS o localhost:**
- MediaRecorder solo funciona en contextos seguros
- Usa `https://` o `http://localhost`

3. **Verificar hardware:**
```bash
# macOS
System Preferences → Sound → Input → Verificar micrófono

# Linux
arecord -l  # Lista micrófonos
```

### ❌ Error: "Audio no se graba"

**Síntomas:**
- Grabación inicia pero archivo está vacío

**Soluciones:**

1. **Verificar formato MIME:**
```javascript
// En consola del navegador:
MediaRecorder.isTypeSupported('audio/webm')  // Debe ser true
```

2. **Probar con otro navegador:**
- Chrome: audio/webm
- Safari: audio/mp4
- Firefox: audio/ogg

### ❌ Error: ffmpeg no encontrado

**Síntomas:**
```
WARNING:root:ffmpeg no disponible
```

**Impacto:**
- Algunos formatos de audio pueden no funcionar

**Solución:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Windows (con Chocolatey)
choco install ffmpeg
```

---

## Transcripción

### ❌ Error: "Error al transcribir audio"

**Síntomas:**
- Transcripción falla con error 500

**Soluciones:**

1. **Verificar logs del servidor:**
```bash
# En la terminal donde corre el servidor
# Buscar líneas con ERROR
```

2. **Verificar formato de audio:**
- Debe ser WAV, WebM, MP3, OGG o M4A
- Sample rate: cualquiera (se convierte a 16kHz)
- Canales: mono o estéreo (se convierte a mono)

3. **Reducir duración:**
- Máximo recomendado: 5 minutos
- Para archivos largos, dividir en segmentos

### ❌ Transcripción incorrecta o vacía

**Síntomas:**
- Texto no coincide con el audio
- Resultado vacío

**Causas comunes:**

1. **Audio de mala calidad:**
- Mucho ruido de fondo
- Volumen muy bajo
- Distorsión

**Soluciones:**
- Grabar en ambiente silencioso
- Hablar claramente y cerca del micrófono
- Verificar volumen de grabación

2. **Idioma incorrecto:**
- El modelo está optimizado para español
- Puede funcionar con otros idiomas pero con menor precisión

3. **Audio muy corto:**
- Mínimo recomendado: 2-3 segundos
- Para frases cortas, agregar contexto

### ❌ Transcripción muy lenta

**Síntomas:**
- Tarda más de 1 minuto por cada 30 segundos de audio

**Causas:**
- Sin aceleración GPU/Metal
- Poca RAM
- Modelo base grande (Voxtral 4B)

**Soluciones:**

1. **Usar versión standalone (más rápida para audio corto):**
```bash
open standalone.html
# Selecciona modelo "Tiny"
```

2. **Cerrar otras aplicaciones:**
```bash
# Liberar RAM y CPU
```

3. **Verificar aceleración (macOS):**
```bash
# En logs del servidor, buscar:
# "Using MPS device"  ← Bueno (GPU)
# "Using CPU device"  ← Lento
```

---

## Red/Conectividad

### ❌ No se puede acceder desde móvil

**Síntomas:**
- `http://localhost:5000` funciona en PC
- `http://IP:5000` no funciona desde móvil

**Soluciones:**

1. **Verificar que están en la misma red WiFi:**
```bash
# PC y móvil deben estar conectados a la misma red
```

2. **Obtener IP correcta:**
```bash
# macOS
ifconfig | grep "inet " | grep -v 127.0.0.1

# Linux
hostname -I

# Windows
ipconfig
```

3. **Verificar firewall:**
```bash
# macOS
System Preferences → Security & Privacy → Firewall
→ Desactivar o permitir Python/Flask

# Linux (UFW)
sudo ufw allow 5000
sudo ufw status
```

4. **Verificar que el servidor escucha en 0.0.0.0:**
```python
# En backend/server.py, línea final:
app.run(host='0.0.0.0', port=5000)  # ✓ Correcto
app.run(host='localhost', port=5000)  # ✗ No funciona desde red
```

### ❌ Error: "No se puede conectar al servidor"

**Síntomas:**
- Frontend muestra "Servidor: Offline"

**Soluciones:**

1. **Verificar que el servidor está corriendo:**
```bash
ps aux | grep python
# Debe mostrar proceso con backend/server.py
```

2. **Verificar puerto:**
```bash
curl http://localhost:5000/health
# Debe retornar: {"status": "ok", ...}
```

3. **Reiniciar servidor:**
```bash
# Ctrl+C para detener
python backend/server.py
```

---

## Rendimiento

### ❌ Frontend muy lento

**Síntomas:**
- UI se congela
- Animaciones lentas

**Soluciones:**

1. **Actualizar navegador:**
- Chrome/Edge 90+
- Firefox 90+
- Safari 14+

2. **Limpiar caché:**
```
Chrome: Ctrl+Shift+Delete
Firefox: Ctrl+Shift+Delete
Safari: Cmd+Option+E
```

3. **Desactivar extensiones:**
- Ad blockers pueden ralentizar
- Probar en modo incógnito

### ❌ Standalone muy lento

**Síntomas:**
- Transcripción tarda minutos

**Causas:**
- Modelo demasiado grande para el dispositivo
- Sin WebGPU

**Soluciones:**

1. **Usar modelo más pequeño:**
- Tiny (~40 MB) → Muy rápido
- Base (~75 MB) → Equilibrado
- Small (~250 MB) → Lento

2. **Verificar WebGPU:**
```
Chrome: chrome://gpu
Buscar: "WebGPU: Hardware accelerated"
```

3. **Habilitar WebGPU (Chrome):**
```
chrome://flags/#enable-unsafe-webgpu
→ Enabled
→ Relaunch
```

---

## Otros problemas

### ❌ Service Worker no se actualiza

**Síntomas:**
- Cambios en código no se ven

**Solución:**
```
1. Abrir DevTools (F12)
2. Application → Service Workers
3. Clic en "Unregister"
4. Recargar página (Ctrl+F5)
```

### ❌ PWA no se puede instalar

**Síntomas:**
- No aparece botón de instalar

**Requisitos para PWA:**
- Servido por HTTPS o localhost
- manifest.json válido
- Service Worker registrado

**Solución:**
```bash
# Verificar manifest:
curl http://localhost:5000/manifest.json

# Verificar en DevTools:
F12 → Application → Manifest
```

---

## 🆘 ¿Nada funcionó?

### Prueba el test suite:

```bash
python test.py
```

Esto verificará:
- ✓ Dependencias instaladas
- ✓ Modelo descargado
- ✓ Backend correcto
- ✓ Frontend completo

### Reporta el bug:

1. Corre: `python test.py > test-output.txt`
2. Incluye logs del servidor
3. Abre un issue en GitHub con:
   - SO y versión
   - Navegador y versión
   - Output del test
   - Logs de error
   - Pasos para reproducir

---

## 📚 Recursos adicionales

- [README.md](README.md) - Documentación completa
- [STANDALONE.md](STANDALONE.md) - Guía versión browser
- [COMPARISON.md](COMPARISON.md) - Comparación versiones
- [QUICKSTART.md](QUICKSTART.md) - Inicio rápido

**¿Encontraste una solución que no está aquí?**
→ Contribuye al proyecto agregándola!
