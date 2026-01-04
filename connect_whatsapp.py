import requests
import base64
import time
import json
import sys

API_URL = "http://localhost:8081"
API_KEY = "AA11BB22"
INSTANCE_NAME = "SalesBot"

def create_instance():
    url = f"{API_URL}/instance/create"
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "instanceName": INSTANCE_NAME,
        "token": "secret-token-123",
        "qrcode": True,
        "integration": "WHATSAPP-BAILEYS"
    }
    
    try:
        print(f"📡 Conectando a {API_URL}...")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 403:
            # Instance might already exist, try to connect/fetch qr
            print("⚠️ La instancia ya existe, intentando conectar...")
            return connect_instance()
            
        if response.status_code != 201 and response.status_code != 200:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False

        data = response.json()
        return process_qr_response(data)

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def connect_instance():
    url = f"{API_URL}/instance/connect/{INSTANCE_NAME}"
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return process_qr_response(data)
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        return False

def process_qr_response(data):
    # Depending on version, QR might be in 'qrcode' or 'base64'
    qr_base64 = None
    
    if 'qrcode' in data and 'base64' in data['qrcode']:
        qr_base64 = data['qrcode']['base64']
    elif 'base64' in data:
        qr_base64 = data['base64']
        
    if qr_base64:
        # Remove header if present
        if "," in qr_base64:
            qr_base64 = qr_base64.split(",")[1]
            
        img_data = base64.b64decode(qr_base64)
        with open("whatsapp_qr.png", "wb") as f:
            f.write(img_data)
        print("✅ QR guardado en: whatsapp_qr.png")
        return True
    else:
        print("⚠️ No se recibió QR (¿Quizás ya está conectada?)")
        print(json.dumps(data, indent=2))
        return False

if __name__ == "__main__":
    create_instance()
