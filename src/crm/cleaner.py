import csv
import os
import re

class DataCleaner:
    CATEGORY_MAP = {
        "electric": "electricista",
        "lampista": "electricista",
        "pintor": "pintor",
        "decor": "pintor",
        "fontan": "fontanero",
        "jardin": "jardinero",
        "carpinter": "carpintero aluminio",
        "cerrajer": "cerrajero",
        "aire": "aire acondicionado",
        "clima": "aire acondicionado",
        "solar": "placas solares",
        "fotov": "placas solares",
        "limpie": "limpieza",
        "reforma": "reformas",
        "baño": "reformas",
        "cocina": "reformas",
        "humedad": "reformas"
    }

    def __init__(self, input_csv, output_csv="data/prospects_cleaned.csv"):
        self.input_csv = input_csv
        self.output_csv = output_csv

    def normalize_phone(self, phone):
        if not phone:
            return None
        
        # Remove all non-digit characters
        clean = re.sub(r'\D', '', phone)
        
        # If empty after cleaning
        if not clean:
            return None
            
        # Basic Validation for Spanish phones (9 digits often starting with 6, 7, 8, 9)
        # If it has 9 digits, prepend 34
        if len(clean) == 9:
            return f"+34{clean}"
            
        # If it starts with 34 and has 11 digits (34 + 9)
        if len(clean) == 11 and clean.startswith("34"):
            return f"+{clean}"
            
        # If it starts with 0034...
        if clean.startswith("0034") and len(clean) == 13:
            return f"+{clean[2:]}"
            
        # Fallback: just return the cleaned digits with + if it looks international
        return f"+{clean}"

    def clean(self):
        if not os.path.exists(self.input_csv):
            print(f"Error: Not found {self.input_csv}")
            return False

        unique_phones = set()
        cleaned_rows = []
        stats = {
            "total": 0,
            "valid": 0,
            "duplicates": 0,
            "missing_phone": 0
        }

        with open(self.input_csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            
            # Ensure new fieldnames has normalized fields if we want to change them, 
            # but usually we just keep strict consistency.
            
            for row in reader:
                stats["total"] += 1
                
                raw_phone = row.get("telefono", "")
                norm_phone = self.normalize_phone(raw_phone)
                
                if not norm_phone:
                    stats["missing_phone"] += 1
                    continue
                
                if norm_phone in unique_phones:
                    stats["duplicates"] += 1
                    continue
                
                unique_phones.add(norm_phone)
                
                # Update row with normalized phone
                row["telefono"] = norm_phone
                # Also ensure 'telefono_normalizado' is set just in case
                row["telefono_normalizado"] = norm_phone
                
                # Normalize category
                raw_cat = row.get("categoria", "").lower()
                norm_cat = "default"
                for search_key, target_key in self.CATEGORY_MAP.items():
                    if search_key in raw_cat:
                        norm_cat = target_key
                        break
                row["categoria"] = norm_cat
                
                cleaned_rows.append(row)
                stats["valid"] += 1

        # Write to output
        if cleaned_rows:
            # Add telefono_normalizado to headers if not present
            if "telefono_normalizado" not in fieldnames:
                fieldnames.append("telefono_normalizado")
                
            with open(self.output_csv, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(cleaned_rows)
                
            print(f"🧹 Data Cleaning Report:")
            print(f"   - Total Rows: {stats['total']}")
            print(f"   - Valid Rows: {stats['valid']}")
            print(f"   - Duplicates Removed: {stats['duplicates']}")
            print(f"   - Missing Phones Removed: {stats['missing_phone']}")
            print(f"   - Output: {self.output_csv}")
            return True
        else:
            print("⚠️ No valid data found.")
            return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/amb_barcelona_sin_web_20260102_223732.csv")
    args = parser.parse_args()
    
    cleaner = DataCleaner(args.input)
    cleaner.clean()
