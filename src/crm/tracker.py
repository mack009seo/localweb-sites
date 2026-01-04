import csv
import os
from datetime import datetime

class ProspectTracker:
    """Gestiona los estados y el historial de contacto de los prospectos usando el módulo csv estándar."""
    
    STATES = ['pending', 'demo_ready', 'contacted', 'interested', 'on_hold', 'converted', 'rejected']

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self._ensure_columns()

    def _ensure_columns(self):
        """Asegura que el CSV tenga las columnas necesarias para el seguimiento."""
        if not os.path.exists(self.csv_file):
            return

        with open(self.csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
        
        required_columns = ['estado', 'fecha_generacion', 'fecha_contacto', 'url_demo', 'notas']
        missing = [col for col in required_columns if col not in fieldnames]
        
        if missing:
            rows = []
            with open(self.csv_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                new_fieldnames = fieldnames + missing
                for row in reader:
                    for col in missing:
                        row[col] = 'pending' if col == 'estado' else ''
                    rows.append(row)
            
            with open(self.csv_file, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=new_fieldnames)
                writer.writeheader()
                writer.writerows(rows)

    def update_status(self, business_name, new_status, demo_url=None, notes=None):
        """Actualiza el estado y metadatos de un negocio. Solo actualiza registros existentes."""
        if new_status not in self.STATES:
            raise ValueError(f"Estado no válido. Debe ser uno de: {self.STATES}")
            
        rows = []
        updated = False
        fieldnames = []
        
        with open(self.csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['nombre'] == business_name:
                    row['estado'] = new_status
                    if demo_url:
                        row['url_demo'] = demo_url
                    if notes:
                        old_notes = row.get('notas', '')
                        row['notas'] = f"{old_notes} | {notes}".strip(' | ')
                    
                    if new_status == 'demo_ready':
                        row['fecha_generacion'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    elif new_status == 'contacted':
                        row['fecha_contacto'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    updated = True
                rows.append(row)
        
        if updated:
            with open(self.csv_file, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            return True
        else:
             print(f"⚠️ Warning: Prospect '{business_name}' not found in tracker. Skipping update.")
             return False

    def get_summary(self):
        """Devuelve un resumen del funnel de ventas."""
        summary = {}
        with open(self.csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                estado = row.get('estado', 'pending')
                summary[estado] = summary.get(estado, 0) + 1
        return summary

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CRM Lite para gestión de prospectos.")
    parser.add_argument("--csv", type=str, default="data/amb_barcelona_sin_web_20260102_223732.csv")
    parser.add_argument("--summary", action="store_true", help="Mostrar resumen del funnel.")
    
    args = parser.parse_args()
    tracker = ProspectTracker(args.csv)
    
    if args.summary:
        print("\n📊 Resumen del Funnel de Ventas:")
        summary = tracker.get_summary()
        for estado in ProspectTracker.STATES:
            count = summary.get(estado, 0)
            if count > 0 or estado == 'pending':
                print(f"  - {estado.capitalize()}: {count}")
