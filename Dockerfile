# Usar Node.js 18 como base (Debian slim para menor tamaño)
FROM node:18-slim

# Instalar dependencias del sistema (Python y herramientas de compilación para Node)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias de Node.js primero (para aprovechar caché de capas)
COPY whatsapp-bridge/package*.json ./whatsapp-bridge/
RUN cd whatsapp-bridge && npm install

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto del bridge
EXPOSE 3001

# Comando para arrancar el bridge
CMD ["node", "whatsapp-bridge/bridge.js"]
