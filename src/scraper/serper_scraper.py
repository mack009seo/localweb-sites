#!/usr/bin/env python3
"""
Scraper de Google Maps usando Serper.dev
Extrae negocios locales en España y Barcelona
"""

import requests
import json
import time
from typing import List, Dict
import csv

class SerperDevScraper:
    """Scraper de Google Maps usando la API de Serper.dev"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        # URL para Google Maps API de Serper.dev
        self.base_url = "https://google.serper.dev/maps"

    def search_local_businesses(
        self,
        keyword: str,
        location: str,
        max_results: int = 20
    ) -> List[Dict]:
        """
        Busca negocios locales en Google Maps

        Args:
            keyword: Tipo de negocio (ej: "fontanero", "reformas cocina")
            location: Ubicación (ej: "Barcelona")
            max_results: Número máximo de resultados

        Returns:
            Lista de diccionarios con datos de negocios
        """
        # Construir consulta
        query = f"{keyword} {location}"

        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        payload = {
            "q": query,
            "type": "local",
            "hl": "es",  # Español
            "gl": "es"   # España
        }

        print(f"🔍 Buscando: {query}")

        try:
            # Serper.dev Maps API usa POST con JSON payload
            payload = {
                "q": query,
                "hl": "es",  # Español
                "gl": "es"   # España
            }

            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                # Debug: guardar respuesta para ver qué devuelve
                print(f"  📄 Claves en respuesta: {list(data.keys())}")
                if "localResults" in data:
                    print(f"  📄 Resultados locales: {len(data['localResults'])}")
                elif "knowledgeGraph" in data:
                    print(f"  📄 KnowledgeGraph encontrado")
                elif "organic" in data:
                    print(f"  📄 Resultados orgánicos: {len(data['organic'])}")

                businesses = self._parse_local_results(data, keyword, location)
                print(f"✓ Encontrados: {len(businesses)} negocios")
                return businesses
            elif response.status_code == 401:
                print("✗ Error: API key inválida")
                return []
            elif response.status_code == 429:
                print("✗ Error: Límite de créditos alcanzado")
                return []
            else:
                print(f"✗ Error HTTP {response.status_code}: {response.text[:200]}")
                return []

        except Exception as e:
            print(f"✗ Error en la petición: {e}")
            return []

    def _parse_local_results(
        self,
        data: Dict,
        keyword: str,
        location: str
    ) -> List[Dict]:
        """
        Extrae y estructura los datos de los resultados locales

        Args:
            data: Respuesta JSON de Serper.dev
            keyword: Palabra clave usada
            location: Ubicación usada

        Returns:
            Lista de negocios estructurados
        """
        businesses = []

        # Serper.dev devuelve resultados en 'localResults' o 'places'
        local_results = data.get("localResults", data.get("places", []))

        for place in local_results[:20]:  # Máximo 20 por búsqueda
            try:
                # Extraer teléfono si está disponible
                phone = place.get("phoneNumber", "")

                # Verificar si tiene sitio web
                website = place.get("website", "")
                has_website = bool(website)

                # Extraer dirección
                address = place.get("address", "")

                # Extraer valoración
                rating = place.get("rating", 0)

                # Extraer número de reseñas
                reviews_count = place.get("reviews", 0)

                # Extraer enlace de Google Maps
                maps_link = place.get("links", {}).get("website", "")

                business = {
                    "nombre": place.get("title", ""),
                    "direccion": address,
                    "telefono": phone,
                    "categoria": keyword,
                    "ubicacion": location,
                    "valoracion": rating,
                    "num_reseñas": reviews_count,
                    "tiene_web": has_website,
                    "website": website,
                    "google_maps_link": maps_link,
                    "tipo": place.get("type", ""),
                }

                businesses.append(business)

            except Exception as e:
                print(f"  ⚠ Error procesando resultado: {e}")
                continue

        return businesses

    def filter_no_website(self, businesses: List[Dict]) -> List[Dict]:
        """Filtra negocios que NO tienen sitio web"""
        return [b for b in businesses if not b["tiene_web"]]

    def filter_by_rating(self, businesses: List[Dict], min_rating: float = 4.0) -> List[Dict]:
        """Filtra negocios por valoración mínima"""
        return [b for b in businesses if b["valoracion"] >= min_rating]

    def save_to_csv(self, businesses: List[Dict], filename: str):
        """Guarda los resultados en un archivo CSV"""
        if not businesses:
            print("⚠ No hay datos para guardar")
            return

        fieldnames = [
            "nombre",
            "direccion",
            "telefono",
            "categoria",
            "ubicacion",
            "valoracion",
            "num_reseñas",
            "tiene_web",
            "website",
            "google_maps_link",
            "tipo",
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(businesses)

        print(f"💾 Guardados {len(businesses)} negocios en: {filename}")

    def print_summary(self, businesses: List[Dict]):
        """Imprime un resumen de los resultados"""
        if not businesses:
            print("📊 No hay resultados para mostrar")
            return

        print(f"\n{'='*60}")
        print(f"📊 RESUMEN DE RESULTADOS")
        print(f"{'='*60}")

        # Total
        total = len(businesses)
        no_web = [b for b in businesses if not b["tiene_web"]]
        high_rating = [b for b in businesses if b["valoracion"] >= 4.0]
        no_web_high_rating = [b for b in businesses if not b["tiene_web"] and b["valoracion"] >= 4.0]

        print(f"\n📈 Totales:")
        print(f"  Total negocios:        {total}")
        print(f"  Sin sitio web:         {len(no_web)} ({len(no_web)/total*100:.1f}%)")
        print(f"  Valoración ≥ 4.0:      {len(high_rating)} ({len(high_rating)/total*100:.1f}%)")
        print(f"  Sin web + ≥ 4.0:       {len(no_web_high_rating)} ({len(no_web_high_rating)/total*100:.1f}%)")

        # Valoración media
        avg_rating = sum(b["valoracion"] for b in businesses) / total if total > 0 else 0
        print(f"\n⭐ Valoración media:      {avg_rating:.2f}/5")

        # Top 5 negocios sin web
        if no_web:
            print(f"\n🎯 TOP 5 NEGOCIOS SIN WEB (por valoración):")
            top_no_web = sorted(no_web, key=lambda x: x["valoracion"], reverse=True)[:5]
            for i, b in enumerate(top_no_web, 1):
                print(f"  {i}. {b['nombre']}")
                print(f"     ⭐ {b['valoracion']}/5 ({b['num_reseñas']} reseñas)")
                print(f"     📞 {b['telefono']}")
                print(f"     📍 {b['direccion']}")
                print()

        print(f"{'='*60}\n")


def main():
    """Función principal para búsqueda extensa"""

    # API key proporcionada
    API_KEY = "2535e56d4ef528df2403585ba37c5ee9f6ccb639"

    scraper = SerperDevScraper(API_KEY)

    # Nichos de MÁXIMO margen en España (ordenados por potencial)
    keywords = [
        # Muy alto margen (20-35%)
        "reformas cocina",
        "reformas baño",
        "reformas integrales",
        "carpintero aluminio",
        "tratamiento humedades",

        # Alto margen (15-25%)
        "fontanero",
        "electricista",
        "aire acondicionado",
        "instalador placas solares",
        "pintor decorator",

        # Buenos nichos (15-20%)
        "jardinero",
        "cerrajero",
        "limpieza fachadas",
    ]

    # Ciudades del área metropolitana de Barcelona (por renta/actividad)
    locations = [
        "Barcelona",
        "L'Hospitalet de Llobregat",
        "Badalona",
        "Sabadell",
        "Terrassa",
        "Mataró",
        "Granollers",
        "Sant Cugat del Vallès",
    ]

    all_businesses = []
    no_web_businesses = []

    print("="*70)
    print("🚀 SCRAPER EXTENSIVO - ÁREA METROPOLITANA BARCELONA")
    print("="*70)
    print(f"📍 Ubicaciones: {len(locations)} ciudades")
    print(f"🔍 Nichos: {len(keywords)} categorías")
    print(f"🔑 API Key: {API_KEY[:20]}...")
    print(f"🎯 Objetivo: 100+ negocios sin web")
    print("="*70)
    print()

    search_count = 0
    for location in locations:
        print(f"\n{'='*70}")
        print(f"📍 CIUDAD: {location}")
        print(f"{'='*70}")

        for keyword in keywords:
            search_count += 1
            businesses = scraper.search_local_businesses(keyword, location)

            # Filtrar los que no tienen web
            no_web = scraper.filter_no_website(businesses)
            no_web_businesses.extend(no_web)

            all_businesses.extend(businesses)

            # Mostrar progreso
            print(f"   → Sin web: {len(no_web)}/{len(businesses)} (Acumulado: {len(no_web_businesses)})")

            # Pausa corta entre búsquedas
            time.sleep(1)

            # Mostrar resumen parcial cada cierto número de búsquedas
            if search_count % 10 == 0:
                print(f"\n   📊 Progreso: {search_count} búsquedas completadas")
                print(f"   🎯 Negocios sin web acumulados: {len(no_web_businesses)}")

    # Guardar todos los resultados
    timestamp = time.strftime("%Y%m%d_%H%M%S")

    if all_businesses:
        filename_all = f"data/amb_barcelona_all_{timestamp}.csv"
        scraper.save_to_csv(all_businesses, filename_all)

    if no_web_businesses:
        filename_no_web = f"data/amb_barcelona_sin_web_{timestamp}.csv"
        scraper.save_to_csv(no_web_businesses, filename_no_web)

    # Resumen final
    print(f"\n{'='*70}")
    print(f"📊 RESUMEN FINAL")
    print(f"{'='*70}")
    print(f"\n📈 Métricas globales:")
    print(f"  Búsquedas realizadas:     {search_count}")
    print(f"  Total negocios:           {len(all_businesses)}")
    print(f"  Sin sitio web:            {len(no_web_businesses)} ({len(no_web_businesses)/len(all_businesses)*100:.1f}%)")

    # Valoración media
    avg_rating = sum(b["valoracion"] for b in all_businesses) / len(all_businesses) if all_businesses else 0
    print(f"  Valoración media:         {avg_rating:.2f}/5")

    # Por ubicación
    print(f"\n📍 Negocios sin web por ciudad:")
    by_city = {}
    for b in no_web_businesses:
        city = b["ubicacion"]
        by_city[city] = by_city.get(city, 0) + 1

    for city, count in sorted(by_city.items(), key=lambda x: x[1], reverse=True):
        print(f"  {city}: {count}")

    # Por categoría
    print(f"\n🏷️ Negocios sin web por categoría:")
    by_category = {}
    for b in no_web_businesses:
        cat = b["categoria"]
        by_category[cat] = by_category.get(cat, 0) + 1

    for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")

    # Top 10 mejores prospectos
    if no_web_businesses:
        print(f"\n🏆 TOP 10 MEJORES PROSPECTOS (sin web):")
        top_prospects = sorted(no_web_businesses, key=lambda x: (x["valoracion"], x["num_reseñas"]), reverse=True)[:10]
        for i, b in enumerate(top_prospects, 1):
            print(f"  {i:2}. {b['nombre'][:40]}")
            print(f"      ⭐ {b['valoracion']}/5 | 📞 {b['telefono']} | 📍 {b['ubicacion']}")

    print(f"\n{'='*70}")
    print(f"✅ ARCHIVOS GENERADOS:")
    if all_businesses:
        print(f"   → {filename_all} ({len(all_businesses)} negocios)")
    if no_web_businesses:
        print(f"   → {filename_no_web} ({len(no_web_businesses)} prospects)")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
