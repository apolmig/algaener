# 🌐 VoxTral PWA - GitHub Pages

## 🚀 Desplegado en GitHub Pages

Esta es la versión **standalone** de VoxTral que funciona 100% en tu navegador.

### ✨ Características

- 🎤 Graba audio desde tu navegador
- 🤖 Transcripción con Whisper AI
- 🔒 100% privado - todo en tu navegador
- 🌐 Sin servidor - funciona offline
- ⚡ WebGPU acelerado

### 📱 Usar la app

**Desde cualquier lugar:**
- [https://apolmig.github.io/algaener/standalone.html](https://apolmig.github.io/algaener/standalone.html)

**O con dominio personalizado:**
- [https://algaener.com/standalone.html](https://algaener.com/standalone.html)

### 🎯 Cómo funciona

1. **Carga modelo** - Selecciona tiny/base/small (primera vez)
2. **Graba audio** - Usa el botón de micrófono
3. **Transcribe** - Procesa el audio con Whisper
4. **Listo** - Tu texto aparece en pantalla

### 📖 Documentación

- [Guía Standalone](STANDALONE.md) - Guía completa
- [Troubleshooting](TROUBLESHOOTING.md) - Solución de problemas
- [GitHub Repo](https://github.com/apolmig/algaener) - Código fuente

### 🔧 Para desarrolladores

Si quieres la versión con **backend** (Voxtral 4B):
```bash
git clone https://github.com/apolmig/algaener.git
cd algaener
./setup.sh
./start.sh
```

Esta versión requiere servidor local/VPS y no funciona en GitHub Pages.

---

**Powered by Transformers.js & Whisper AI**
