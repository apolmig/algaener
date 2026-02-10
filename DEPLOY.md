# 🚀 Guía de Despliegue - VoxTral PWA

Esta guía cubre todos los métodos de despliegue para VoxTral PWA.

---

## 📑 Índice

1. [GitHub Pages](#-github-pages-gratis) ⭐ Recomendado para standalone
2. [Servidor Local](#-servidor-local) - Para desarrollo
3. [VPS/Cloud](#-vpscloud) - Para versión backend
4. [Docker](#-docker) - Containerizado

---

## 🌐 GitHub Pages (Gratis)

### ✅ Lo que funciona

**Versión Standalone:**
- ✅ `standalone.html` - 100% funcional
- ✅ Transformers.js + Whisper
- ✅ Grabación de audio
- ✅ PWA instalable
- ✅ HTTPS automático
- ✅ Sin costos

### ❌ Lo que NO funciona

**Versión Backend:**
- ❌ Flask/Python server
- ❌ Modelo Voxtral 4B
- ❌ API REST endpoints

### 📋 Configuración paso a paso

#### 1. Preparar repositorio

El repo ya está configurado:
```
✅ index.html - Redirección automática a standalone
✅ standalone.html - App principal
✅ manifest-standalone.json - PWA config
✅ .nojekyll - Evita procesamiento Jekyll
✅ frontend/icon.svg - Icono de la app
```

#### 2. Habilitar GitHub Pages

```bash
# Opción A: Desde GitHub.com
1. Ve a tu repo: https://github.com/apolmig/algaener
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: main (o claude/review-codebase-C59f4)
5. Folder: / (root)
6. Save
```

```bash
# Opción B: Desde terminal (gh CLI)
gh repo edit --enable-pages --pages-branch main
```

#### 3. Configurar dominio personalizado (opcional)

Si tienes `algaener.com`:

1. En tu proveedor de DNS, agrega:
```
Type: CNAME
Name: @ (o www)
Value: apolmig.github.io
```

2. En GitHub Pages settings:
```
Custom domain: algaener.com
Enforce HTTPS: ✓
```

#### 4. Verificar despliegue

Espera 2-3 minutos, luego accede a:
```
https://apolmig.github.io/algaener/
```

O con dominio personalizado:
```
https://algaener.com/
```

### 🔧 Troubleshooting GitHub Pages

**Error: "404 Page not found"**
```bash
# Verifica que la branch esté correcta
git branch -a

# Verifica que index.html exista
ls -la index.html

# Fuerza un rebuild
git commit --allow-empty -m "Trigger rebuild"
git push
```

**Error: "Manifest no carga"**
```bash
# Verifica rutas relativas en manifest-standalone.json
# Deben ser: "./standalone.html" no "/standalone.html"
```

**Error: "Service Worker falla"**
```bash
# En standalone.html, asegúrate que no registre SW
# O crea un sw.js en la raíz
```

---

## 💻 Servidor Local

### Para desarrollo y testing

```bash
# Método 1: Python simple
python3 -m http.server 8000
# Accede: http://localhost:8000/standalone.html

# Método 2: Node.js (si tienes npm)
npx serve .
# Accede: http://localhost:3000/standalone.html

# Método 3: PHP
php -S localhost:8000
# Accede: http://localhost:8000/standalone.html
```

### Para versión Backend (Flask + Voxtral)

```bash
# Instalación completa
./setup.sh

# Iniciar servidor
./start.sh

# O manualmente:
source venv/bin/activate
python backend/server.py

# Accede: http://localhost:5000
```

---

## ☁️ VPS/Cloud

### Para versión Backend con producción

#### Requisitos de servidor

- **CPU**: 4+ cores
- **RAM**: 16GB+ (32GB recomendado)
- **Disco**: 20GB+ SSD
- **OS**: Ubuntu 22.04 / Debian 11 / macOS
- **GPU**: Opcional (NVIDIA para CUDA, o Apple Silicon para Metal)

#### Proveedores recomendados

| Proveedor | Precio/mes | RAM | Notas |
|-----------|-----------|-----|-------|
| DigitalOcean | $48 | 16GB | Droplet básico |
| Hetzner | €30 | 16GB | Mejor precio/rendimiento |
| AWS EC2 | $50+ | 16GB | t3.xlarge |
| Google Cloud | $50+ | 16GB | n2-standard-4 |

#### Instalación en VPS

```bash
# 1. SSH al servidor
ssh user@tu-servidor.com

# 2. Clonar repo
git clone https://github.com/apolmig/algaener.git
cd algaener

# 3. Instalar
./setup.sh

# 4. Configurar como servicio (systemd)
sudo nano /etc/systemd/system/voxtral.service
```

**Contenido del servicio:**
```ini
[Unit]
Description=VoxTral PWA Backend
After=network.target

[Service]
Type=simple
User=tu-usuario
WorkingDirectory=/home/tu-usuario/algaener
Environment="PATH=/home/tu-usuario/algaener/venv/bin"
ExecStart=/home/tu-usuario/algaener/venv/bin/python backend/server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 5. Activar servicio
sudo systemctl enable voxtral
sudo systemctl start voxtral
sudo systemctl status voxtral

# 6. Configurar nginx (reverse proxy)
sudo apt install nginx
sudo nano /etc/nginx/sites-available/voxtral
```

**Configuración nginx:**
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# 7. Activar y reiniciar nginx
sudo ln -s /etc/nginx/sites-available/voxtral /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# 8. Configurar HTTPS (opcional pero recomendado)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

---

## 🐳 Docker

### Versión Backend containerizada

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    wget \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Descargar modelo (o montarlo como volumen)
# RUN ./download_model.sh

# Exponer puerto
EXPOSE 5000

# Comando de inicio
CMD ["python", "backend/server.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  voxtral:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./voxtral-model:/app/voxtral-model
    environment:
      - VOXTRAL_MODEL_DIR=/app/voxtral-model
      - HOST=0.0.0.0
      - PORT=5000
    restart: unless-stopped
```

**Uso:**
```bash
# Build
docker-compose build

# Descargar modelo (fuera del contenedor)
./download_model.sh

# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## 🎯 Recomendaciones por caso de uso

### Uso personal / Demo
→ **GitHub Pages** (standalone.html)
- Gratis
- Sin configuración
- Acceso global

### Desarrollo local
→ **Servidor local**
- Fácil testing
- Sin exponer a internet
- Desarrollo rápido

### Producción pequeña (5-50 usuarios)
→ **VPS básico**
- DigitalOcean/Hetzner
- 16GB RAM
- Backend completo

### Producción grande (50+ usuarios)
→ **VPS potente + Load Balancer**
- 32GB RAM
- GPU dedicada
- Múltiples instancias

### Máxima portabilidad
→ **Docker**
- Fácil de mover
- Consistente entre ambientes
- Escalable

---

## 📊 Comparación de despliegue

| Método | Costo | Complejidad | Velocidad | Funcionalidad |
|--------|-------|-------------|-----------|---------------|
| GitHub Pages | $0 | ⭐ | Rápido | Solo standalone |
| Local | $0 | ⭐⭐ | Muy rápido | Completa |
| VPS | $30-50/mes | ⭐⭐⭐ | Rápido | Completa |
| Docker | Variable | ⭐⭐⭐⭐ | Rápido | Completa |

---

## ✅ Checklist de despliegue

### GitHub Pages
- [ ] Habilitar Pages en settings
- [ ] Verificar que index.html existe
- [ ] Probar URL: https://usuario.github.io/repo/
- [ ] Configurar dominio personalizado (opcional)
- [ ] Verificar que HTTPS está activo

### VPS
- [ ] Servidor con requisitos mínimos
- [ ] Clonar repositorio
- [ ] Ejecutar ./setup.sh
- [ ] Descargar modelo
- [ ] Configurar servicio systemd
- [ ] Configurar nginx/reverse proxy
- [ ] Configurar HTTPS con Let's Encrypt
- [ ] Configurar firewall (puerto 80/443)
- [ ] Probar desde internet

### Docker
- [ ] Crear Dockerfile
- [ ] Crear docker-compose.yml
- [ ] Build imagen
- [ ] Descargar modelo
- [ ] docker-compose up
- [ ] Verificar logs
- [ ] Probar endpoints

---

## 🆘 Ayuda

Si tienes problemas:

1. Consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Revisa logs del servidor
3. Verifica firewall/puertos
4. Abre issue en GitHub

---

## 📚 Recursos adicionales

- [GitHub Pages docs](https://docs.github.com/pages)
- [DigitalOcean tutorials](https://www.digitalocean.com/community/tutorials)
- [Nginx docs](https://nginx.org/en/docs/)
- [Docker docs](https://docs.docker.com/)

---

**¿Listo para desplegar?** Elige el método que mejor se adapte a tu caso de uso y sigue la guía paso a paso.
