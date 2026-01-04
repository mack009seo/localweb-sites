
import csv
import urllib.parse
from src.messaging.outreach_manager import OutreachManager

def print_examples():
    om = OutreachManager()
    
    print("\n--- 5 Ejemplos de Mensajes Generados ---\n")
    
    count = 0
    with open('data/prospects_cleaned.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if count >= 5:
                break
                
            localidad = row.get('ubicacion', 'su ciudad')
            if not localidad:
                localidad = 'Barcelona' # Fallback default
                
            # Simulate the slug generation as done in other scripts
            slug = row['nombre'].lower().replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
            slug = ''.join(c for c in slug if c.isalnum() or c == '-')
            
            # Get the link
            link = om.get_whatsapp_link(
                row['telefono'],
                row['nombre'],
                row['categoria'],
                slug,
                localidad
            )
            
            # Decode the text parameter from the link to show the actual message
            parsed = urllib.parse.urlparse(link)
            query_params = urllib.parse.parse_qs(parsed.query)
            message_text = query_params['text'][0]
            
            print(f"🔹 EJEMPLO {count + 1}: {row['nombre']}")
            print("-" * 40)
            print(message_text)
            print("-" * 40)
            print("\n")
            
            count += 1

if __name__ == "__main__":
    print_examples()
