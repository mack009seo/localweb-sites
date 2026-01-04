#!/usr/bin/env python3
import csv
import os
import re
from datetime import datetime

def normalize_phone(phone):
    """Normaliza el teléfono al formato +34XXXXXXXXX."""
    if not phone or str(phone).strip() == "":
        return None
    
    # Extraer solo dígitos
    digits = re.sub(r'\D', '', str(phone))
    
    # Si tiene 9 dígitos, asumimos que es español y le falta el prefijo
    if len(digits) == 9:
        return f"+34{digits}"
    # Si tiene 11 dígitos y empieza por 34
    if len(digits) == 11 and digits.startswith('34'):
        return f"+{digits}"
    
    # Si no encaja, devolvemos los dígitos con un + por si acaso
    if len(digits) > 7:
        return f"+{digits}" if not digits.startswith('+') else digits
        
    return digits

def clean_data():
    data_dir = "data"
    output_file = os.path.join(data_dir, "cleaned_prospects_BARCELONA.csv")
    
    # Listar archivos CSV
    csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv") and "cleaned" not in f]
    print(f"Archivos encontrados: {csv_files}")
    
    all_rows = []
    headers = []
    
    for file in csv_files:
        filepath = os.path.join(data_dir, file)
        try:
            with open(filepath, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if not headers:
                    headers = reader.fieldnames
                for row in reader:
                    row['source_file'] = file
                    all_rows.append(row)
            print(f"Cargado {file} con {len(all_rows)} registros totales acumulados.")
        except Exception as e:
            print(f"Error cargando {file}: {e}")
            
    if not all_rows:
        print("No se encontraron datos para procesar.")
        return
        
    initial_count = len(all_rows)
    print(f"Total inicial de registros: {initial_count}")
    
    # 1. Normalización y Limpieza
    processed_rows = []
    for row in all_rows:
        # Normalizar teléfono
        row['telefono_normalizado'] = normalize_phone(row.get('telefono', ''))
        
        # Limpiar dirección
        direccion = row.get('direccion', '')
        if direccion:
            row['direccion'] = direccion.replace(", España", "").strip()
            
        # Normalizar valoración y reseñas
        try:
            row['valoracion'] = float(row.get('valoracion', 0) or 0)
        except:
            row['valoracion'] = 0.0
            
        try:
            row['num_reseñas'] = int(row.get('num_reseñas', 0) or 0)
        except:
            row['num_reseñas'] = 0
            
        processed_rows.append(row)
        
    # 2. Eliminación de duplicados
    # Ordenar por reseñas y valoración para quedarnos con el "mejor" duplicado
    processed_rows.sort(key=lambda x: (x['num_reseñas'], x['valoracion']), reverse=True)
    
    duplicates_by_phone = {}
    duplicates_by_name_addr = {}
    final_rows = []
    
    for row in processed_rows:
        tel = row['telefono_normalizado']
        name = row.get('nombre', '').lower().strip()
        addr_short = row.get('direccion', '')[:20].lower().strip()
        
        is_duplicate = False
        
        if tel:
            if tel in duplicates_by_phone:
                is_duplicate = True
            else:
                duplicates_by_phone[tel] = True
        
        # Si no tiene teléfono o no es duplicado por teléfono, chequear por nombre+dirección
        if not is_duplicate:
            key = f"{name}|{addr_short}"
            if key in duplicates_by_name_addr:
                is_duplicate = True
            else:
                duplicates_by_name_addr[key] = True
                
        if not is_duplicate:
            final_rows.append(row)
            
    # 3. Enriquecimiento final
    for i, row in enumerate(final_rows):
        row['prospect_id'] = f"BCN-{i+1:04d}"
        row['status'] = "pending"
        row['date_added'] = datetime.now().strftime("%Y-%m-%d")
        
    # Definir orden de columnas
    base_cols = ['prospect_id', 'nombre', 'categoria', 'telefono_normalizado', 'telefono', 'direccion', 'ubicacion', 'valoracion', 'num_reseñas', 'status', 'date_added', 'google_maps_link']
    
    # Asegurarse de incluir todas las columnas originales y nuevas
    all_fields = list(base_cols)
    for row in final_rows:
        for key in row.keys():
            if key not in all_fields:
                all_fields.append(key)
                
    # Guardar CSV
    with open(output_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_fields)
        writer.writeheader()
        writer.writerows(final_rows)
        
    final_count = len(final_rows)
    print(f"\nProceso completado (usando módulo csv estándar):")
    print(f"- Registros iniciales: {initial_count}")
    print(f"- Duplicados eliminados: {initial_count - final_count}")
    print(f"- Registros finales: {final_count}")
    print(f"- Archivo guardado: {output_file}")

if __name__ == "__main__":
    clean_data()
