# Guía de Despliegue en Producción: LocalPro WhatsApp Bridge 🚀

Esta guía detalla los pasos para poner en marcha el bridge de WhatsApp (Baileys) y el procesador de mensajes (Python) en un servidor Linux (se recomienda Ubuntu 22.04 o superior).

## 📋 Requisitos Previos

- Un servidor con acceso SSH.
- Node.js v18+ y npm instalados.
- Python 3.10+ y pip instalados.
- Un número de WhatsApp disponible (se recomienda un número nuevo o uno de empresa).

---

## 🛠️ Paso 1: Preparación del Servidor

1. **Clonar el repositorio:**
   ```bash
   git clone [URL_DEL_REPOSITORIO] /home/llorens/00Code/localweb
   cd /home/llorens/00Code/localweb
   ```

2. **Configurar variables de entorno:**
   Crea el archivo `.env` en la raíz (si no existe) con tu API Key de Gemini:
   ```bash
   GEMINI_API_KEY="tu_clave_aqui"
   ```

---

## 🐍 Paso 2: Configuración de Python

1. **Crear y activar entorno virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install google-generativeai requests
   ```

---

## 📦 Paso 3: Configuración del Bridge (Node.js)

1. **Instalar dependencias de Node:**
   ```bash
   cd whatsapp-bridge
   npm install
   ```

2. **Instalar PM2 para gestión de procesos:**
   ```bash
   sudo npm install -g pm2
   ```

---

## 🚀 Paso 4: Lanzamiento en Producción

1. **Iniciar el Bridge con PM2:**
   Desde la carpeta `whatsapp-bridge/`:
   ```bash
   pm2 start bridge.js --name "whatsapp-bridge"
   ```

2. **Vincular WhatsApp:**
   - Abre el puerto 3001 en tu firewall o usa un túnel/SSH.
   - Accede a `http://tu-servidor:3001/qr` en tu navegador.
   - Escanea el código QR con tu aplicación de WhatsApp.

3. **Verificar logs:**
   Asegúrate de que no haya errores:
   ```bash
   pm2 logs whatsapp-bridge
   ```

---

## 🌐 Paso 5: Nginx (Opcional pero Recomendado)

Para acceder de forma segura y usar un dominio, configura un proxy inverso en Nginx:

```nginx
server {
    listen 80;
    server_name bridge.localpro.top;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
}
```

---

## 🐋 Paso 6: Despliegue con Docker (Coolify / VPS)

Si usas **Coolify** o prefieres Docker, utiliza los archivos `Dockerfile` y `docker-compose.yml` incluidos en la raíz.

### En Coolify:
1.  **Crear un nuevo recurso:** Selecciona "Docker Compose".
2.  **Configurar origen:** Conecta tu repositorio de GitHub/GitLab.
3.  **Variables de entorno:** Añade `GEMINI_API_KEY` en la pestaña "Environment Variables".
4.  **Almacenamiento (Storage):** Coolify detectará automáticamente el volumen definido en el `docker-compose.yaml` para persistir la sesión.
5.  **Desplegar:** Pulsa "Deploy".

### Manualmente con Docker Compose:
```bash
docker-compose up -d --build
```

---

## 🔍 Notas de Mantenimiento

- **Persistencia:** Si el servidor se reinicia, usa `pm2 save` and `pm2 startup` para que el bridge vuelva a arrancar solo.
- **Autenticación:** Los datos de sesión se guardan en `whatsapp-bridge/auth_info_baileys`. No borres esta carpeta a menos que quieras volver a escanear el QR.
- **Python Bridge:** El archivo `bridge.js` llama a `python3 ../src/messaging/process_incoming.py`. Asegúrate de que el comando `python3` apunte al entorno correcto o usa la ruta absoluta del binario del `venv`.

> **Seguridad:** No expongas el puerto 3001 al público sin seguridad si vas a usar la API de envío de mensajes desde fuera del servidor. Usa Nginx con autenticación básica o IP whitelist.

---

## 🆘 Resolución de Problemas y Alternativas a Coolify

Si el despliegue automático en Coolify falla (generalmente por falta de RAM o cortes de red durante el `npm install`), tienes estas alternativas sólidas y gratuitas (o muy baratas) para mantener tu bot 24/7.

### Opción A (Recomendada): Docker Directo en tu VPS 🐳
Si ya tienes el VPS (donde tienes Coolify), **esta es la opción más robusta y gratuita**. Te saltas la capa de construcción de Coolify y corres los contenedores directamente "al hierro".

**Pasos:**
1.  **Entra a tu servidor por SSH:**
    ```bash
    ssh usuario@tu-ip
    ```
2.  **Clona el repo (si no lo tienes):**
    ```bash
    git clone https://github.com/mack009seo/localweb-sites.git
    cd localweb-sites
    ```
3.  **Lanza el bot:**
    ```bash
    # Asegúrate de tener tu .env con la API KEY primero
    echo "GEMINI_API_KEY=tu_api_key_real" > .env
    
    # Levanta los contenedores en segundo plano
    docker compose up -d --build
    ```
4.  **Vincula WhatsApp:**
    - Averigua tu IP pública.
    - Entra en `http://TU_IP:3001/qr` y escanea. 
    - ¡Listo! Funciona igual que en Coolify pero sin intermediarios.

### Opción B: Railway (PaaS Gestionado) 🚂
Excelente alternativa si no quieres gestionar servidores. Tiene un plan "Hobby" muy barato y un periodo de prueba.
1.  Entra en [Railway.app](https://railway.app/).
2.  "New Project" > "Deploy from GitHub repo".
3.  Añade la variable `GEMINI_API_KEY`.
4.  Crea un volumen persistente para `/app/whatsapp-bridge/auth_info_baileys` (Vital para no perder la sesión).

### Opción C: Fly.io (Capa Gratuita) 🪰
Permite desplegar Docker apps cerca de tus usuarios.
1.  Instala `flyctl`.
2.  `fly launch` en tu carpeta del proyecto.
3.  Asegúrate de configurar un volumen persistente de 1GB (que suele ser gratis).

