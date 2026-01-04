import urllib.parse
import os
import requests
import json

class OutreachManager:
    """Genera mensajes y enlaces de WhatsApp personalizados para prospectos."""

    def __init__(self, base_url="https://localpro.top/"):
        self.base_url = base_url
        self.api_url = "http://localhost:8081"
        self.api_key = "AA11BB22"
        self.instance_name = "SalesBot"

    def get_whatsapp_link(self, phone, business_name, category, demo_slug, localidad="Barcelona"):
        """Genera un enlace de WhatsApp con un mensaje pre-rellenado."""
        demo_url = f"{self.base_url}{demo_slug}/"
        
        mensaje = (
            f"Hola. He visto el negocio *{business_name}* en *{localidad}* y las buenas opiniones que tiene "
            f"como *{category}*. Se nota que hacéis un buen trabajo. 👍\n\n"
            f"He visto que ahora mismo no tenéis página web, y hoy en día mucha gente busca en Google "
            f"antes de llamar a un profesional. 📱\n\n"
            f"Por eso he preparado una *página web sencilla y profesional* para vuestro negocio:\n"
            f"🔗 {demo_url}\n\n"
            f"Incluye:\n"
            f"• Diseño adaptado a móviles\n"
            f"• Botón para llamar o escribir por WhatsApp ({phone})\n"
            f"• Lista para usar con vuestro propio dominio\n\n"
            f"Es una opción **muy económica** (os sorprenderá el precio).\n"
            f"Contestadme por aquí para ver las opciones y precios sin compromiso."
        )
        
        # Codificar el mensaje para URL
        mensaje_encoded = urllib.parse.quote(mensaje)
        
        # Limpiar el teléfono (quitar espacios, +, etc. para el enlace wa.me)
        phone_clean = ''.join(filter(str.isdigit, phone))
        
        return f"https://wa.me/{phone_clean}?text={mensaje_encoded}"

    def send_whatsapp_message(self, phone, message):
        # El bridge de Baileys espera un POST a http://localhost:3000/send
        api_url = "http://localhost:3001/send"
        
        # Limpiar el número de teléfono solo si no es ya un JID (contiene @)
        if "@" in phone:
            phone_clean = phone
        else:
            phone_clean = "".join(filter(str.isdigit, phone))
        
        payload = {
            "number": phone_clean,
            "text": message
        }
        
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                print(f"✅ Mensaje enviado a {phone}")
                return True
            else:
                print(f"❌ Error enviando a {phone}: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error de conexión con el bridge de Baileys: {str(e)}")
            return False

    def generate_outreach_report(self, prospects):
        """Genera una lista de acciones de contacto para el usuario."""
        report = []
        for p in prospects:
            localidad = p.get('localidad', 'su ciudad') # Fallback seguro
            link = self.get_whatsapp_link(
                p['telefono'], 
                p['nombre'], 
                p['categoria'], 
                p['nombre'].lower().replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n'),
                localidad
            )
            report.append({
                "nombre": p['nombre'],
                "telefono": p['telefono'],
                "wa_link": link
            })
        return report

if __name__ == "__main__":
    # Test rápido
    om = OutreachManager()
    link = om.get_whatsapp_link("+34 600 000 000", "Pintores Pérez", "Pintor", "pintores-perez")
    print(f"Link generado:\n{link}")
