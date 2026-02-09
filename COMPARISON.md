# 🆚 Comparación: Standalone vs Backend

## Tabla comparativa rápida

| Característica | 🌐 Standalone | 🚀 Backend (Voxtral) |
|----------------|---------------|----------------------|
| **Instalación** | ✅ Ninguna (abre HTML) | ⚠️ Python + dependencias |
| **Descarga inicial** | 40-250 MB | 9 GB |
| **Servidor requerido** | ❌ No | ✅ Sí (Flask) |
| **Funciona offline** | ✅ Sí (después de cargar) | ✅ Sí |
| **Acceso remoto** | ❌ No (solo local) | ✅ Sí (LAN/WiFi) |
| **Velocidad** | ⚡⚡ Rápida | ⚡⚡⚡ Muy rápida |
| **Precisión** | ★★★ Buena | ★★★★ Excelente |
| **Modelo IA** | Whisper tiny/base/small | Voxtral Realtime 4B |
| **Aceleración** | WebGPU / WASM | Metal / BLAS / GPU |
| **Uso de RAM** | ~500 MB - 2 GB | ~8 GB - 16 GB |
| **Navegador** | Cualquiera moderno | Cualquiera |
| **SO compatible** | Windows/Mac/Linux/iOS/Android | Mac/Linux (Windows exp.) |

## 📊 Rendimiento

### Tiempo de transcripción (audio de 30 segundos)

**Standalone (Whisper)**
- Tiny + WebGPU: ~2-3 segundos
- Base + WebGPU: ~5-8 segundos
- Tiny + CPU: ~10-15 segundos

**Backend (Voxtral 4B)**
- Con Metal (M3): ~2-3 segundos
- Con BLAS: ~5-10 segundos

## 🎯 Casos de uso

### Usa **Standalone** cuando:
- ✅ Quieres probar rápidamente
- ✅ No quieres instalar nada
- ✅ Uso ocasional (pocas transcripciones)
- ✅ Compartir con otros (enviar link/archivo)
- ✅ Dispositivo con espacio limitado
- ✅ No tienes Python instalado
- ✅ Necesitas máxima portabilidad
- ✅ Demos o presentaciones

### Usa **Backend** cuando:
- ✅ Uso intensivo diario
- ✅ Necesitas máxima precisión
- ✅ Archivos largos (>5 minutos)
- ✅ Múltiples dispositivos accediendo
- ✅ Integración con otros sistemas
- ✅ Producción / trabajo profesional
- ✅ Tienes los recursos (RAM, GPU)
- ✅ Quieres la mejor experiencia

## 💻 Requisitos mínimos

### Standalone
- **CPU**: Cualquiera moderno (2015+)
- **RAM**: 4 GB (8 GB recomendado)
- **Espacio**: 500 MB
- **Navegador**: Chrome 90+, Firefox 90+, Safari 14+
- **OS**: Cualquiera (Windows/Mac/Linux/iOS/Android)

### Backend
- **CPU**: Multi-core moderno
- **RAM**: 16 GB (32 GB recomendado)
- **Espacio**: 15 GB
- **GPU**: Opcional pero muy recomendada
- **OS**: macOS (mejor), Linux, Windows (experimental)

## 📈 Calidad de transcripción

### Precisión típica

| Condición | Standalone (Base) | Backend (Voxtral) |
|-----------|-------------------|-------------------|
| Audio limpio | ~90-95% | ~95-98% |
| Con ruido leve | ~80-85% | ~90-95% |
| Con ruido fuerte | ~60-70% | ~75-85% |
| Múltiples voces | ~70-80% | ~85-90% |
| Acentos | ~80-90% | ~90-95% |

*Nota: Valores aproximados, varían según audio*

## 🚀 Inicio rápido

### Standalone (2 pasos)
```bash
# 1. Abrir archivo
open standalone.html

# 2. En el navegador:
#    - Cargar modelo
#    - Grabar
#    - Transcribir
# ¡Listo!
```

### Backend (3 pasos)
```bash
# 1. Instalar
./setup.sh

# 2. Iniciar servidor
source venv/bin/activate
python backend/server.py

# 3. Abrir navegador
# http://localhost:5000
```

## 💡 Recomendación general

### Para la mayoría de usuarios:
**Empieza con Standalone** → Si necesitas más, usa Backend

### Flujo recomendado:
1. Prueba `standalone.html` primero
2. Si te gusta y la usas frecuentemente
3. Considera instalar la versión Backend
4. Usa Backend para trabajo serio
5. Mantén Standalone para demostraciones

## 🔄 ¿Puedo usar ambas?

**¡Sí!** Las dos versiones son independientes y complementarias:

- **Standalone** para demos, pruebas, uso móvil
- **Backend** para trabajo diario en tu PC/Mac

No interfieren entre sí. Puedes tener ambas instaladas.

## 📝 Resumen ejecutivo

**¿Cuál elegir?**

| Tu situación | Recomendación |
|--------------|---------------|
| "Solo quiero probar" | 🌐 **Standalone** |
| "Uso ocasional" | 🌐 **Standalone** |
| "No tengo Python" | 🌐 **Standalone** |
| "Poca RAM/espacio" | 🌐 **Standalone** |
| "Uso diario" | 🚀 **Backend** |
| "Trabajo profesional" | 🚀 **Backend** |
| "Archivos largos" | 🚀 **Backend** |
| "Máxima calidad" | 🚀 **Backend** |

**¿Aún con dudas?**
→ Empieza con Standalone. Es gratis y toma 30 segundos probarlo.

---

Ver guías completas:
- [Standalone Guide](STANDALONE.md)
- [Backend Guide](README.md)
