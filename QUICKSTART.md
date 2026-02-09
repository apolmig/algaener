# 🚀 Inicio Rápido - VoxTral PWA

## Instalación en 3 pasos

### 1️⃣ Instalar

```bash
./setup.sh
```

### 2️⃣ Iniciar

```bash
source venv/bin/activate
python backend/server.py
```

### 3️⃣ Usar

Abre en tu navegador: **http://localhost:5000**

---

## Desde móvil

1. Encuentra tu IP local:
   ```bash
   hostname -I  # Linux
   ipconfig getifaddr en0  # macOS
   ```

2. En el móvil, abre: **http://TU_IP:5000**

3. Instala como app:
   - Menú (⋮) → "Agregar a pantalla de inicio"

---

## Problemas comunes

### ❌ Error: No se puede conectar al servidor
- Verifica que el servidor esté corriendo
- Usa la IP correcta, no `localhost` desde móvil
- Verifica el firewall

### ❌ Error: Modelo no encontrado
```bash
./download_model.sh
```

### ❌ Error: Permisos de micrófono
- Permite acceso al micrófono en tu navegador
- Chrome → Configuración → Privacidad → Permisos

---

## Uso básico

1. **Grabar** → Habla
2. **Detener** → Cuando termines
3. **Transcribir** → Espera el resultado
4. **Copiar** → Usa la transcripción

¡Eso es todo! 🎉

---

Para más detalles, lee el [README.md](README.md) completo.
