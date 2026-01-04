
import sys
import os
from sales_bot import SalesBot
from outreach_manager import OutreachManager

def process_message(sender, text):
    print(f"🐍 Procesando mensaje de {sender}: {text}")
    
    # Initialize components
    bot = SalesBot()
    om = OutreachManager()
    
    # Generate response
    response_text = bot.generate_response(text)
    
    print(f"🐍 Respuesta generada: {response_text}")
    
    # Send response back
    # The sender from Baileys is usually 'number@s.whatsapp.net'
    # OutreachManager.send_whatsapp_message figures out the cleaning
    success = om.send_whatsapp_message(sender, response_text)
    
    if success:
        print(f"✅ Respuesta enviada con éxito a {sender}")
    else:
        print(f"❌ Fallo al enviar respuesta a {sender}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 process_incoming.py [sender] [text]")
        sys.exit(1)
        
    sender_jid = sys.argv[1]
    message_text = " ".join(sys.argv[2:])
    
    process_message(sender_jid, message_text)
