# 🌐 VoxTral Browser - Versión 100% Standalone

## ⚡ Sin servidor, sin backend, sin instalación

Esta versión funciona **completamente en el navegador** usando [Transformers.js](https://github.com/xenova/transformers.js) con modelos Whisper de OpenAI.

## ✨ Características

- 🌐 **100% en el navegador** - No necesita servidor backend
- 🚀 **WebGPU acelerado** - Usa GPU cuando está disponible
- 🔒 **Totalmente privado** - Todo el audio se procesa localmente
- 📦 **Sin instalación** - Solo abre el archivo HTML
- 🌍 **Funciona offline** - Una vez descargado el modelo
- ⚡ **Modelos múltiples** - Elige entre tiny, base o small

## 🎯 Uso Rápido

### Opción 1: Abrir directamente

```bash
# Simplemente abre el archivo en tu navegador
open standalone.html
```

O haz doble clic en `standalone.html`

### Opción 2: Servidor local simple

```bash
# Python 3
python3 -m http.server 8000

# Luego abre: http://localhost:8000/standalone.html
```

### Opción 3: Hospedar en GitHub Pages

1. Sube `standalone.html` a tu repositorio
2. Habilita GitHub Pages
3. Accede desde cualquier lugar: `https://tu-usuario.github.io/tu-repo/standalone.html`

## 📖 Cómo funciona

### 1. Cargar modelo

Al abrir la aplicación:
1. Selecciona un modelo Whisper:
   - **Tiny** (40MB) - Muy rápido, precisión aceptable
   - **Base** (75MB) - Equilibrado (recomendado)
   - **Small** (250MB) - Más preciso, más lento

2. Clic en "🚀 Cargar Modelo"
3. Espera a que se descargue (solo la primera vez)

### 2. Grabar y transcribir

1. **Grabar** - Presiona el botón del micrófono
2. **Habla** - El audio se graba localmente
3. **Detener** - Para la grabación
4. **Transcribir** - Procesa el audio con Whisper
5. **Resultado** - El texto aparece en pantalla

## 🚀 Modelos disponibles

| Modelo | Tamaño | Velocidad | Precisión | Uso recomendado |
|--------|--------|-----------|-----------|------------------|
| **Tiny** | ~40 MB | ⚡⚡⚡ | ★★☆ | Testing, demos rápidas |
| **Base** | ~75 MB | ⚡⚡☆ | ★★★ | Uso general (recomendado) |
| **Small** | ~250 MB | ⚡☆☆ | ★★★★ | Máxima precisión |

## 🔧 Aceleración

La app detecta automáticamente las capacidades de tu dispositivo:

- **WebGPU** ⚡ - Usa GPU si está disponible (Chrome/Edge modernos)
- **WebAssembly** 💻 - Fallback rápido en CPU
- **CPU puro** - Funciona en cualquier navegador moderno

### Navegadores con WebGPU

| Navegador | Soporte WebGPU |
|-----------|----------------|
| Chrome 113+ | ✅ |
| Edge 113+ | ✅ |
| Firefox | 🚧 En desarrollo |
| Safari | 🚧 Experimental |

## 💾 Uso de datos

### Primera vez
- Descarga el modelo seleccionado (~40-250 MB)
- Se guarda en caché del navegador
- No se vuelve a descargar

### Después
- Usa el modelo desde caché
- **0 bytes de red** para transcribir
- Todo local

## 📱 Instalación como PWA

### En móvil (Chrome/Safari)
1. Abre `standalone.html` en el navegador
2. Menú (⋮) → "Agregar a pantalla de inicio"
3. ¡Listo! Funciona como app nativa

### En escritorio (Chrome/Edge)
1. Icono de instalación (⊕) en la barra de dirección
2. "Instalar"
3. Se abre como ventana independiente

## 🔒 Privacidad

### ✅ Lo que ocurre localmente
- Grabación de audio
- Procesamiento con Whisper
- Transcripción completa
- Almacenamiento de resultados

### ❌ Lo que NUNCA sale del navegador
- Tu audio
- Tus transcripciones
- Datos personales

### 🌐 Lo único que se descarga
- Modelo Whisper (primera vez, desde HuggingFace CDN)
- Librería Transformers.js (desde jsDelivr CDN)

## ⚡ Optimización

### Para mejor rendimiento:

1. **Usa Chrome/Edge con WebGPU**
   - Verifica en: chrome://gpu
   - Debe decir "WebGPU: Hardware accelerated"

2. **Empieza con modelo Tiny**
   - Prueba velocidad
   - Sube a Base/Small si necesitas más precisión

3. **Grabaciones cortas**
   - Óptimo: 10-30 segundos
   - Máximo recomendado: 2 minutos

4. **Dispositivo potente**
   - PC/Mac moderno: cualquier modelo
   - Móvil: mejor usar Tiny o Base

## 🆚 Comparación: Standalone vs Backend

| Característica | Standalone | Backend (Voxtral) |
|----------------|------------|-------------------|
| Instalación | Ninguna | Python + 9GB modelo |
| Servidor | No necesario | Flask requerido |
| Red | Solo descarga inicial | LAN requerida |
| Velocidad | Rápida (WebGPU) | Muy rápida (GPU/Metal) |
| Precisión | Buena | Excelente |
| Modelos | Whisper tiny/base/small | Voxtral 4B |
| Uso | Casual, demos | Producción, uso intensivo |

## 🐛 Solución de problemas

### "No se puede cargar el modelo"
- Verifica conexión a internet (primera vez)
- Limpia caché del navegador
- Prueba con otro modelo (más pequeño)

### "Error al acceder al micrófono"
- Permite permisos de micrófono
- Solo funciona con HTTPS o localhost
- Verifica que no esté en uso por otra app

### "Transcripción muy lenta"
- Prueba con modelo más pequeño (Tiny)
- Verifica si WebGPU está activo
- Cierra otras pestañas pesadas

### "Audio no se graba"
- Verifica permisos del navegador
- Prueba con otro navegador
- Comprueba que el micrófono funcione

## 🎓 Casos de uso

### ✅ Perfecto para:
- Demos rápidas
- Testing de speech-to-text
- Transcripciones ocasionales
- Uso en dispositivos sin Python
- Compartir con otros (link directo)
- Privacidad máxima

### ⚠️ Considera backend para:
- Uso intensivo diario
- Archivos de audio largos (>5 min)
- Máxima precisión requerida
- Procesamiento batch
- Integración con otros sistemas

## 🔗 Enlaces útiles

- [Transformers.js](https://github.com/xenova/transformers.js) - Librería usada
- [Whisper](https://github.com/openai/whisper) - Modelo de OpenAI
- [WebGPU](https://developer.chrome.com/blog/webgpu-release/) - Aceleración GPU

## 📊 Estadísticas

### Tiempo de carga inicial
- Tiny: ~5-10 segundos
- Base: ~10-20 segundos
- Small: ~30-60 segundos

### Tiempo de transcripción (30 seg audio)
- **Con WebGPU (GPU)**
  - Tiny: ~2-3 segundos
  - Base: ~5-8 segundos
  - Small: ~15-20 segundos

- **Sin WebGPU (CPU)**
  - Tiny: ~10-15 segundos
  - Base: ~30-45 segundos
  - Small: ~90-120 segundos

## 🚀 Despliegue

### GitHub Pages (gratis)

1. Crear repositorio en GitHub
2. Subir `standalone.html`
3. Settings → Pages → Enable
4. Acceder: `https://usuario.github.io/repo/standalone.html`

### Netlify/Vercel (gratis)

1. Conectar repositorio
2. Deploy automático
3. URL personalizada

### Tu propio servidor

```bash
# Cualquier servidor web estático funciona
python3 -m http.server 8000
# o
npx serve .
```

## 📄 Licencia

MIT - Igual que el proyecto principal

---

**¡Disfruta de la transcripción de audio sin límites!** 🎉

Para la versión con backend completo y Voxtral, revisa [README.md](README.md)
