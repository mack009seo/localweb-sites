# Comparativa APIs y Librerías para Scraping de Google Maps
## Enfocado en Negocios con Alto Margen (2025)

---

## Índice
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Comparativa de APIs con Plan Gratuito](#comparativa-apis)
3. [Librerías Python para Scraping Directo](#librerias-python)
4. [Negocios con Alto Margen para Enfocar](#negocios-alto-margen)
5. [Análisis Costo-Beneficio](#analisis-costo-beneficio)
6. [Recomendaciones Finales](#recomendaciones)

---

## Resumen Ejecutivo

### Mejores Opciones por Caso de Uso

| Caso de Uso | Opción Recomendada | Motivo |
|-------------|-------------------|--------|
| **Prueba rápida** | Serper.dev | 2,500 créditos gratis al registrarte |
| **Producción económica** | Playwright + Proxies | Gratis, solo costo de proxies |
| **Producción sin mantenimiento** | Outscraper | $0.002/registro, más barato a escala |
| **Alto volumen** | SearchAPI | $1,500 por 1M búsquedas vs $7,000 de SerpAPI |
| **Balance precio/calidad** | Scrapingdog | 1,000 créditos gratis + $40/mes inicio |

---

## Comparativa de APIs con Plan Gratuito

### Tabla Comparativa Principal

| API | Plan Gratuito | Inicio Pago | Costo/1K Búsquedas | Datos que Obtiene |
|-----|---------------|-------------|-------------------|-------------------|
| **Serper.dev** | 2,500 créditos | $0.001/scrape | ~$1 | ★★★★☆ Nombre, dirección, teléfono, web, rating |
| **Scrapingdog** | 1,000 créditos | $40/mes (40K) | ~$1 | ★★★★★ Todos los datos + email |
| **Outscraper** | 500 registros | Pay-as-you-go | $2 | ★★★★★ Excelente para Google Maps específico |
| **SerpAPI** | 100 búsquedas/mes | $50/mes (5K) | $10-15 | ★★★★☆ Datos completos + reseñas |
| **Apify** | 500 resultados | ~$1/1K | $1 | ★★★★☆ Plataforma fácil de usar |
| **ZenRows** | 50 búsquedas/mes | $4.20/1K | $4.20 | ★★★☆☆ Básico, requiere proxies |
| **Zenserp** | 50 búsquedas/mes | $49.99/mes (5K) | $10 | ★★★☆☆ SERP general |
| **SearchAPI** | Contactar | $1,500/1M | $1.50 | ★★★★★ Mejor valor alto volumen |

### Detalle por API

#### 1. Serper.dev ⭐ MEJOR PLAN GRATUITO

```
Plan Gratuito: 2,500 créditos al registrarte
Precio: $0.001 por scrape (baja escala)
      $0.00075 por scrape (alta escala)

Ventajas:
✓ Más generoso plan gratuito
✓ Respuestas muy rápidas (<200ms)
✓ Ligero y fácil de integrar
✓ Ideal para pruebas y desarrollo

Desventajas:
✗ Menos funciones específicas de Maps
✗ Requiere integración adicional para reseñas
```

**Código de ejemplo:**
```python
import requests

# Serper.dev para Google Maps
url = "https://google.serper.dev/search"
payload = json.dumps({
    "q": "fence contractor in New Jersey",
    "type": "local"
})
headers = {
    'X-API-KEY': 'TU_API_KEY',
    'Content-Type': 'application/json'
}
response = requests.post(url, headers=headers, data=payload)
```

#### 2. Scrapingdog ⭐ MEJOR BALANCE

```
Plan Gratuito: 1,000 créditos/mes
Precio: $40/mes por 40,000 créditos

Ventajas:
✓ Balance generoso entre gratis/pago
✓ 100% success rate en benchmarks
✓ Proporciona emails adicionales
✓ Tiempo respuesta: ~3s

Desventajas:
✗ Requiere plan pago para volumen
✗ Menos documentación que SerpAPI
```

**Costo por conversión:** Si conviertes al 10%, cada cliente te cuesta $4 en scraping.

#### 3. Outscraper ⭐ MEJOR PARA GOOGLE MAPS ESPECÍFICO

```
Plan Gratuito: 500 registros/mes (Google Maps)
Precio: $0.002 por registro después

Ventajas:
✓ Especializado en Google Maps/Reviews
✓ Precio por registro muy económico
✓ Excelente calidad de datos
✓ API bien documentada

Desventajas:
✗ Plan gratuito más pequeño
✗ Reiere plan pago para volumen significativo
```

**Cálculo de costo:**
- 10,000 negocios = $20
- 100,000 negocios = $200

#### 4. SerpAPI

```
Plan Gratuito: 100 búsquedas/mes
Precio: $50/mes por 5,000 búsquedas
      $150/mes por 15,000 búsquedas
      $7,000/mes por 1,000,000 búsquedas

Ventajas:
✓ Muy popular, bien documentado
✓ Datos completos + reseñas
✓ Estable y confiable

Desventajas:
✗ Más caro que alternativas
✗ Plan gratuito muy limitado
✗ No escala bien en precio
```

**Comparación de escala:**
- SerpAPI: $7,000 por 1M búsquedas
- SearchAPI: $1,500 por 1M búsquedas
- DataForSEO: $600 por 1M búsquedas

#### 5. Apify

```
Plan Gratuito: 500 resultados/mes
Precio: Pay-as-you-go (~$0.50-$1 por 1,000 resultados)

Ventajas:
✓ Interfaz drag-and-drop
✓ Herramientas pre-construidas
✓ Fácil para no-programadores

Desventajas:
✗ Requiere proxies residenciales (pago)
✗ Tiempo de configuración
✗ Menos control que código directo
```

---

## Librerías Python para Scraping Directo

### Opción 1: Playwright ⭐ RECOMENDADO 2025

**Velocidad:** 2-3x más rápido que Selenium
**Éxito en Google Maps:** ★★★★★

```python
from playwright.sync_api import sync_playwright
import time

def scrape_google_maps_playwright(keyword, location):
    with sync_playwright() as p:
        # Lanzar navegador en modo stealth
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()

        # Navegar a Google Maps
        page.goto("https://www.google.com/maps")
        time.sleep(2)

        # Buscar
        page.fill('input[placeholder="Search Google Maps"]', f"{keyword} in {location}")
        page.press('input[placeholder="Search Google Maps"]', "Enter")
        time.sleep(5)

        # Extraer resultados (scroll para cargar más)
        businesses = []
        for _ in range(5):  # Scroll 5 veces
            page.evaluate("window.scrollBy(0, 1000)")
            time.sleep(2)

        # Extraer datos del DOM
        results = page.query_selector_all("div[role='article']")
        for result in results[:20]:  # Primeros 20
            try:
                name = result.query_selector("fontHeadline").text_content()
                rating = result.query_selector("span[aria-label*='star']").get_attribute("aria-label")
                has_website = bool(result.query_selector("a[data-tooltip='Website']"))

                businesses.append({
                    "name": name,
                    "rating": rating,
                    "has_website": has_website
                })
            except:
                continue

        browser.close()
        return businesses

# Uso
businesses = scrape_google_maps_playwright("fence contractor", "New Jersey")
```

**Pros:**
- ✓ 100% GRATIS (solo requiere tu computadora)
- ✓ 2-3x más rápido que Selenium
- ✓ Mejor manejo de contenido dinámico
- ✓ Modo stealth incluido
- ✓ Soporte para múltiples navegadores

**Contras:**
- ✗ Requiere proxies rotativos para volumen alto
- ✗ Google puede bloquear IPs después de ~50-100 búsquedas
- ✗ Requiere mantenimiento si Google cambia el DOM

**Costo de proxies (necesario para volumen):**
- Proxy residencial: $3-5 por GB
- Para 10,000 búsquedas: ~$50-100 en proxies

---

### Opción 2: Selenium

**Velocidad:** Lento pero estable
**Éxito en Google Maps:** ★★★☆☆

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_google_maps_selenium(keyword, location):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.google.com/maps")
    time.sleep(3)

    search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search Google Maps']")
    search_box.send_keys(f"{keyword} in {location}")
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    # Extraer resultados...
    businesses = []
    results = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")

    for result in results[:20]:
        # Extraer datos...
        pass

    driver.quit()
    return businesses
```

**Pros:**
- ✓ GRATIS
- ✓ Muy documentado
- ✓ Comunidad grande

**Contras:**
- ✗ Más lento que Playwright
- ✗ Más fácil de detectar por Google
- ✗ Requiere más mantenimiento

---

### Opción 3: Bibliotecas Específicas

#### google-search-results (no oficial)

```python
from google_search_results import GoogleSearch

params = {
    "engine": "google_maps",
    "q": "fence contractor in New Jersey",
    "type": "search",
    "api_key": "TU_API_KEY"  # Requiere API key
}

client = GoogleSearch(params)
results = client.get_dict()
```

---

## Negocios con Alto Margen para Enfocar

### Top 10 Categorías por Margen de Profit

| Rank | Categoría | Margen Neto | Tamaño Proyecto Medio | Ticket Web Anual |
|------|-----------|-------------|----------------------|------------------|
| 1 | **HVAC** | 10-25% | $8,000-15,000 | **$3,000** |
| 2 | **Plumbing** | 15-20% | $3,000-8,000 | **$3,000** |
| 3 | **Electrical** | 15-25% | $2,000-10,000 | **$3,000** |
| 4 | **Roofing** | 20-35% | $5,000-20,000 | **$3,000** |
| 5 | **Fencing** | 15-25% | $3,000-10,000 | **$3,000** |
| 6 | **Landscaping/Hardscaping** | 15-20% | $5,000-15,000 | **$3,000** |
| 7 | **Solar Installation** | 20-30% | $15,000-30,000 | **$3,000** |
| 8 | **Concrete/Foundation** | 15-20% | $5,000-20,000 | **$3,000** |
| 9 | **Pool Installation** | 20-25% | $20,000-50,000 | **$3,000** |
| 10 | **Kitchen/Bath Remodel** | 20-35% | $15,000-40,000 | **$3,000** |

### Por Qué Estas Categorías Pueden Pagar $3,000/año

#### Análisis ROI para el Negocio

```
Ejemplo: Contratista de Vallas (Fencing)

Ingreso promedio por proyecto: $5,000
Margen neto: 20% = $1,000 profit/proyecto

Si el sitio web genera SOLO 1 cliente adicional cada 3 meses:
- 4 clientes/año extra
- $20,000 en ingresos adicionales
- $4,000 en profit adicional
- Costo del sitio: $3,000/año
- ROI: 133% en el primer año
```

#### Bases de Datos Enfocadas por Categoría

```
Alta Prioridad (Margen Alto + Ticket Alto):
├── HVAC Contractors
├── Solar Panel Installers
├── Pool Builders
├── Kitchen/Bath Remodelers
├── Custom Home Builders

Prioridad Media (Buen Margen + Buen Ticket):
├── Roofing Contractors
├── Fence Contractors
├── Concrete Contractors
├── Landscaping Companies
├── Tree Service (Arbolists)

Prioridad Baja (Volumen Alto + Ticket Bajo):
├── Handymen
├── Cleaning Services
├── Landscaping Maintenance
└── Pest Control
```

### Palabras Clave para Google Maps por Categoría

```python
HIGH_MARGIN_KEYWORDS = [
    # Muy Alto Margen
    "hvac contractor",
    "solar panel installer",
    "custom pool builder",
    "kitchen remodeling",

    # Alto Margen
    "roofing contractor",
    "fence contractor",
    "concrete contractor",
    "foundation repair",

    # Buen Margen
    "electrician",
    "plumber",
    "hardscaping contractor",
    "tree service",
    "deck builder",
]

# Ubicaciones Objetivo (por ingreso promedio)
HIGH_VALUE_LOCATIONS = [
    "New Jersey",
    "New York",
    "Connecticut",
    "Massachusetts",
    "California",
    "Washington",
]
```

---

## Análisis Costo-Beneficio

### Escenario 1: Usando API Pagada (Serper.dev/Scrapingdog)

```
Costos mensuales:
├── API (10,000 búsquedas): $40
├── Claude API (generación sitios): $20
├── Twilio (500 SMS): $25
├── GitHub Pages: $0
└── Total: $85/mes

Métricas:
├── Prospects contactados: 500/mes
├── Tasa respuesta: 20% = 100 respuestas
├── Tasa conversión: 10% = 10 clientes
├── Ingreso: 10 × $3,000 = $30,000
├── Costo/adquisición: $85 ÷ 10 = $8.50
└── ROI: 35,100%

Conclusión: ✓ Muy viable
```

### Escenario 2: Scraper Propio con Playwright + Proxies

```
Costo único:
├── Desarrollo: 20-40 horas
├── Proxies residenciales: $50-100/mes (para volumen)
├── Servidor VPS: $10/mes (opcional, para ejecutar 24/7)
└── Total inicial: ~$100-150/mes

Métricas:
├── Prospects ilimitados
├── Sin costo por búsqueda
├── Mantenimiento: 2-4 horas/mes
└── Escala infinitamente

Conclusión: ✓ Mejor opción a largo plazo
```

### Escenario 3: Híbrido (Recomendado)

```
Fase 1 (Mes 1-2): Usar API con plan gratuito
├── Serper.dev: 2,500 búsquedas gratis
├── Enfocarse en 1-2 categorías
├── Validar el modelo
└── Costo: $0

Fase 2 (Mes 3-6): API pagada o scraper propio
├── Si funciona: Migrar a Playwright + Proxies ($100/mes)
├── Si no tiene tiempo: API pagada ($40-85/mes)
└── Escalar a 10,000+ búsquedas/mes

Conclusión: ✓✓ Mejor balance riesgo/recompensa
```

---

## Recomendaciones Finales

### Por Etapa del Proyecto

#### Etapa 1: Prototipo (Semana 1-2)
**Usar: Serper.dev**
- 2,500 búsquedas gratis
- Validar que el modelo funciona
- Probar 1-2 categorías
- Sin costo inicial

#### Etapa 2: MVP (Mes 1-3)
**Usar: Scrapingdog o Playwright**

| Opción | Cuándo Elegirla |
|--------|-----------------|
| **Scrapingdog** | Tienes presupuesto, quieres rapidez, no quieres mantener código |
| **Playwright** | Tienes tiempo, quieres escalar, prefieres control total |

#### Etapa 3: Producción (Mes 3+)
**Usar: Playwright + Proxies Rotativos**

```python
# Arquitectura recomendada para producción
┌─────────────────────────────────────────────────────────┐
│                  SISTEMA DE PRODUCCIÓN                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐  │
│  │  PLAYWRIGHT  │───▶│  PROXIES     │───▶│  DATA    │  │
│  │  SCRAPER     │    │  ROTATIVOS   │    │  CLEANER │  │
│  └──────────────┘    └──────────────┘    └──────────┘  │
│         │                                      │        │
│         ▼                                      ▼        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐  │
│  │  RATE LIMIT  │    │  ERROR       │    │  CSV/DB  │  │
│  │  HANDLER     │    │  RECOVERY    │    │  EXPORT  │  │
│  └──────────────┘    └──────────────┘    └──────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘

Costo mensual: $100-150 (proxies + hosting)
Capacidad: Ilimitada
```

### Tabla de Decisión Rápida

| Tu Situación | Recomendación |
|--------------|---------------|
| Solo quiero probar | Serper.dev (gratis) |
| Tengo $50/mes presupuesto | Scrapingdog API |
| Quiero escalar ilimitadamente | Playwright + proxies |
| No quiero mantener código | Outscraper API |
| Tengo tiempo pero no dinero | Playwright solo |
| Quiero empezar YA | Serper.dev → migrar después |

---

## Plan de Implementación Recomendado

### Mes 1: Validación con API Gratuita

```bash
# Paso 1: Obtener créditos gratis
- Serper.dev: 2,500 créditos
- Scrapingdog: 1,000 créditos
- Total: 3,500 búsquedas

# Paso 2: Enfocarse en ALTO MARGEN
Keywords = ["hvac contractor", "roofing contractor", "fence contractor"]
Locations = ["New Jersey", "New York"]

# Paso 3: Ejecutar
python src/scraper/api_scraper.py --api serper --keyword "hvac" --location "New Jersey"

# Resultado esperado:
- ~200-300 prospectos calificados
- ~50-100 sin website
- 5-10 demos creadas
- 1-3 conversiones ($3,000-9,000)
```

### Mes 2-3: Decisión de Escala

```
Si conversión > 5%:
    → Invertir en Playwright + proxies ($100/mes)
    → Escalar a todas las categorías de alto margen
    → Objetivo: 50-100 conversiones/mes

Si conversión < 5%:
    → Optimizar el mensaje y la demo
    → Probar diferentes categorías
    → Mantener API pagada ($40-85/mes)
```

### Presupuesto por Etapa

```
MES 1: $0 (créditos gratis)
├── APIs: Gratis
├── Desarrollo: Tu tiempo
└── Hosting demo: Gratis (GitHub Pages)

MES 2-3: $40-85/mes
├── API: $40-50
├── Mensajería: $25
└── Claude: $20

MES 4+: $100-150/mes (si escala)
├── Proxies: $50-100
├── Servidor: $10
├── Mensajería: $25
└── Claude: $20
```

---

## Fuentes Consultadas

### APIs y Scraping
- [5 Best Google Maps Scraper APIs: Tested & Ranked - ScrapingDog](https://www.scrapingdog.com/blog/best-google-maps-scraper/)
- [How to Scrape Google Maps: A Step-By-Step Tutorial 2025 - Decodo](https://decodo.com/blog/google-maps-scraping)
- [Google Maps Scraper Examples (Python & Node.js) - GitHub HasData](https://github.com/HasData/google-maps-scraper)
- [Google SERP API - Free Tier - Outscraper](https://outscraper.com/google-serp-api/)
- [ScraperAPI Pricing - Free 1,000 credits/month](https://www.scraperapi.com/pricing/)
- [Compare Plans and Get Started for Free - ScraperAPI Pricing](https://www.scraperapi.com/pricing/)
- [Zenserp API Pricing - Affordable Search APIs](https://zenserp.com/pricing-plans/)

### Librerías Python
- [Google Maps Scraper Examples (Python & Node.js)](https://github.com/HasData/google-maps-scraper)
- [How to Scrape Google Maps Data with Python - Medium](https://medium.com/@datajournal/how-to-scrape-google-maps-with-python-510dbcca4e92)
- [How Playwright automates Google Maps data scraping - LinkedIn](https://www.linkedin.com/posts/shakib-absar-_datascience-webscraping-streamlit-activity-7215767841382285312-gqIE)
- [How to Scrape Google Reviews Using Python - Scrap.io](https://scrap.io/scrape-google-maps-reviews-python)

### Negocios de Alto Margen
- [Top 5 Most Profitable Home Services Niches In 2025 - HookAgency](https://hookagency.com/blog/most-profitable-home-services-niches/)
- [The Top 8 Most Profitable Home Service Businesses - Owned and Operated](https://www.ownedandoperated.com/post/the-top-8-most-profitable-home-service-businesses-to-start-right-now)
- [Your Guide to HVAC Business Profit Margins - Jobber Academy](https://www.getjobber.com/academy/hvac/hvac-business-profit-margins/)
- [Understanding HVAC Profit Margins - ServiceTitan](https://www.servicetitan.com/blog/hvac-profit-margins)
- [What's a Good Profit Margin for a Plumbing Business? - GoDuo](https://www.goduo.co/blog/whats-a-good-profit-margin-for-a-plumbing-business)
- [Construction Profit Margin vs Markup: Guide - Buildern](https://buildern.com/resources/blog/construction-profit-margin-vs-markup/)
- [35 Most Profitable Construction Business Ideas For 2025 - Connecteam](https://connecteam.com/e-construction-business-ideas/)

---

**Documento creado:** 2025-01-02
**Actualización recomendada:** Cada 3 meses (precios cambian)
