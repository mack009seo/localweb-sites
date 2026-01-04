# Usar Node.js 18 completo para mayor compatibilidad
FROM node:18-bullseye

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Configurar npm para mayor tolerancia
RUN npm config set fetch-retry-maxtimeout 120000 && \
    npm config set fetch-retries 5

# Moverse a la carpeta del bridge e instalar
WORKDIR /app/whatsapp-bridge
COPY whatsapp-bridge/package*.json ./
RUN npm install --legacy-peer-deps --verbose

# Volver a la raíz para el resto del proyecto
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

COPY . .

# Exponer el puerto del bridge
EXPOSE 3001

# Comando para arrancar el bridge
CMD ["node", "whatsapp-bridge/bridge.js"]
