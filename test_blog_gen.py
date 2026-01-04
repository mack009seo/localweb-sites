from src.generator.site_generator import StaticSiteGenerator

generator = StaticSiteGenerator("data/cleaned_prospects_BARCELONA.csv")
# We manually pass the first row data to test
test_prospect = {
    'prospect_id': 'BCN-0001',
    'nombre': 'Carpinteria de aluminio Jos-mar SL.',
    'categoria': 'carpintero aluminio',
    'telefono': '+34 934 11 02 90',
    'direccion': 'Carrer de Cardó, 9, Sants-Montjuïc, 08028 Barcelona',
    'ubicacion': 'Barcelona',
    'valoracion': '5.0',
    'num_reseñas': '0'
}

slug = generator.generate_site(test_prospect)
print(f"Generated site slug: {slug}")
