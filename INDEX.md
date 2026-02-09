# 📑 Índice de archivos - VoxTral PWA

## 🚀 Para empezar AHORA

### Opción 1: Solo quiero probar (RECOMENDADO)
```
📄 Abre: standalone.html
```
**Eso es todo.** Se abre en tu navegador y funciona inmediatamente.

### Opción 2: Instalación completa con backend
```
📖 Lee: QUICKSTART.md
```
O ejecuta: `./setup.sh`

---

## 📚 Documentación

| Archivo | Descripción | Para quién |
|---------|-------------|------------|
| **[standalone.html](standalone.html)** | 🌐 App completa en navegador | **TODOS** - Empieza aquí |
| **[QUICKSTART.md](QUICKSTART.md)** | ⚡ Inicio rápido backend | Si quieres instalar el backend |
| **[STANDALONE.md](STANDALONE.md)** | 📖 Guía standalone completa | Para entender la versión de navegador |
| **[README.md](README.md)** | 📘 Documentación completa | Referencia completa del backend |
| **[COMPARISON.md](COMPARISON.md)** | 🆚 Comparación versiones | ¿No sabes cuál elegir? |

---

## 🎯 Guía rápida por situación

### "Solo quiero probarlo"
→ Abre [standalone.html](standalone.html)

### "¿Cuál versión necesito?"
→ Lee [COMPARISON.md](COMPARISON.md)

### "Quiero instalar el backend"
→ Sigue [QUICKSTART.md](QUICKSTART.md)

### "Necesito ayuda con standalone"
→ Lee [STANDALONE.md](STANDALONE.md)

### "Quiero toda la info del backend"
→ Lee [README.md](README.md)

---

## 📂 Estructura del proyecto

```
algaener/
│
├── 📄 standalone.html          ← ¡EMPIEZA AQUÍ!
│
├── 📚 Documentación
│   ├── INDEX.md               ← Este archivo
│   ├── QUICKSTART.md          ← Inicio rápido backend
│   ├── STANDALONE.md          ← Guía standalone
│   ├── README.md              ← Docs completas backend
│   └── COMPARISON.md          ← Comparación
│
├── 🎨 Frontend (PWA)
│   ├── frontend/
│   │   ├── index.html         ← UI principal backend
│   │   ├── css/style.css
│   │   ├── js/app.js
│   │   ├── manifest.json
│   │   └── sw.js
│   └── manifest-standalone.json
│
├── ⚙️ Backend (Python)
│   └── backend/
│       ├── server.py          ← Servidor Flask
│       └── voxtral_inference.py
│
├── 🛠️ Instalación
│   ├── setup.sh               ← Script de instalación
│   ├── download_model.sh      ← Descargar modelo Voxtral
│   └── requirements.txt
│
└── 📝 Config
    ├── .gitignore
    ├── CNAME
    ├── LICENSE
    └── _config.yml
```

---

## ⚡ TL;DR (Muy corto)

**¿Primera vez?**
1. Abre `standalone.html`
2. Carga modelo "Base"
3. Graba audio
4. Transcribe

**¿Quieres más potencia?**
1. `./setup.sh`
2. `python backend/server.py`
3. Abre http://localhost:5000

---

## 🤔 FAQ rápido

**P: ¿Cuál abro primero?**
R: `standalone.html` - funciona inmediatamente

**P: ¿Necesito instalar algo?**
R: No para standalone, sí para backend

**P: ¿Cuál es mejor?**
R: Standalone para probar, Backend para trabajo serio
Lee [COMPARISON.md](COMPARISON.md)

**P: ¿Puedo usar ambas?**
R: Sí, son independientes

**P: ¿Funciona en móvil?**
R: Sí, ambas versiones

---

**¿Listo?** → Abre [standalone.html](standalone.html) y empieza en 30 segundos 🚀
