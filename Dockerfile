# Usar Node.js 18 Bullseye (Debian 11) para máxima estabilidad
FROM node:18-bullseye

# Instalar Python y dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Configurar npm para evitar errores de red y memoria
RUN npm config set fetch-retry-maxtimeout 120000 && \
    npm config set fetch-retries 5

# Copiar archivos de dependencia de Node
COPY whatsapp-bridge/package.json ./whatsapp-bridge/

# Instalar dependencias ignorando el lockfile y con logs
RUN cd whatsapp-bridge && \
    rm -f package-lock.json && \
    npm install --no-package-lock --verbose

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto del bridge
EXPOSE 3001

# Comando para arrancar el bridge
CMD ["node", "whatsapp-bridge/bridge.js"]
