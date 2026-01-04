# Comparativa APIs y Librerías para Scraping de Google Maps
## Enfocado en Negocios de Alto Margen en España y Barcelona (2025)

---

## Índice
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Comparativa de APIs con Plan Gratuito](#comparativa-apis)
3. [Librerías Python para Scraping Directo](#librerias-python)
4. [Nichos de Alto Margen en España](#nichos-alto-margen-espana)
5. [Análisis Costo-Beneficio en Euros](#analisis-costo-beneficio)
6. [Plan de Acción para Barcelona](#plan-accion-barcelona)
7. [Recomendaciones Finales](#recomendaciones)

---

## Resumen Ejecutivo

### Mejores Opciones por Caso de Uso

| Caso de Uso | Opción Recomendada | Motivo |
|-------------|-------------------|--------|
| **Prueba rápida** | Serper.dev | 2.500 créditos gratis al registrarte |
| **Producción económica** | Playwright + Proxies | Gratis, solo costo de proxies |
| **Producción sin mantenimiento** | Outscraper | 0,50€-2€ por 1.000 registros |
| **Alto volumen** | SearchAPI | Mejor valor a gran escala |
| **Balance precio/calidad** | Scrapingdog | 1.000 créditos gratis + ~37€/mes |

---

## Comparativa de APIs con Plan Gratuito

### Tabla Comparativa Principal

| API | Plan Gratuito | Inicio Pago | Costo/1K Búsquedas | Datos que Obtiene |
|-----|---------------|-------------|-------------------|-------------------|
| **Serper.dev** | 2.500 créditos | 0,001€/búsqueda | ~1€ | ★★★★☆ Nombre, dirección, teléfono, web, valoración |
| **Scrapingdog** | 1.000 créditos | 37€/mes (40K) | ~0,93€ | ★★★★★ Todos los datos + email |
| **Outscraper** | 500 registros | Pago por uso | 0,50€-2€ | ★★★★★ Excelente para Google Maps específico |
| **SerpAPI** | 100 búsquedas/mes | 46€/mes (5K) | 9-14€ | ★★★★☆ Datos completos + reseñas |
| **Apify** | 500 resultados | ~0,93€/1K | 0,93€ | ★★★★☆ Plataforma fácil de usar |
| **ZenRows** | 50 búsquedas/mes | 44€/mes (5K) | 8,80€ | ★★★☆☆ Básico, requiere proxies |
| **Zenserp** | 50 búsquedas/mes | 46€/mes (5K) | 9,20€ | ★★★☆☆ SERP general |
| **SearchAPI** | Contactar | 1.400€/1M | 1,40€ | ★★★★★ Mejor valor alto volumen |

### Detalle por API

#### 1. Serper.dev ⭐ MEJOR PLAN GRATUITO

```
Plan Gratuito: 2.500 créditos al registrarte
Precio: 0,001€ por búsqueda (baja escala)
      0,00075€ por búsqueda (alta escala)

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
import json

# Serper.dev para Google Maps
url = "https://google.serper.dev/search"
payload = json.dumps({
    "q": "instalador aire acondicionado Barcelona",
    "type": "local",
    "hl": "es"  # Español
})
headers = {
    'X-API-KEY': 'TU_API_KEY',
    'Content-Type': 'application/json'
}
response = requests.post(url, headers=headers, data=payload)
results = response.json()
```

#### 2. Scrapingdog ⭐ MEJOR BALANCE

```
Plan Gratuito: 1.000 créditos/mes
Precio: 37€/mes por 40.000 créditos

Ventajas:
✓ Balance generoso entre gratis/pago
✓ 100% tasa de éxito en benchmarks
✓ Proporciona emails adicionales
✓ Tiempo respuesta: ~3s

Desventajas:
✗ Requiere plan pago para volumen
✗ Menos documentación que SerpAPI
```

**Cálculo de costo (España):**
- 10.000 negocios = 9,30€
- 100.000 negocios = 93€

#### 3. Outscraper ⭐ MEJOR PARA GOOGLE MAPS ESPECÍFICO

```
Plan Gratuito: 500 registros/mes (Google Maps)
Precio: 0,002€ por registro después

Ventajas:
✓ Especializado en Google Maps/Reseñas
✓ Precio por registro muy económico
✓ Excelente calidad de datos
✓ API bien documentada

Desventajas:
✗ Plan gratuito más pequeño
✗ Requiere plan pago para volumen significativo
```

---

## Librerías Python para Scraping Directo

### Opción 1: Playwright ⭐ RECOMENDADO 2025

**Velocidad:** 2-3x más rápido que Selenium
**Éxito en Google Maps:** ★★★★★

```python
from playwright.sync_api import sync_playwright
import time
import json

def scrape_google_maps_playwright(keyword, location):
    """
    Scraper de Google Maps con Playwright para España

    Args:
        keyword: Palabra clave (ej: "aire acondicionado")
        location: Ubicación (ej: "Barcelona")

    Returns:
        Lista de diccionarios con datos de negocios
    """
    with sync_playwright() as p:
        # Lanzar navegador en modo stealth
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            locale="es-ES"
        )
        page = context.new_page()

        # Navegar a Google Maps
        page.goto("https://www.google.com/maps")
        time.sleep(2)

        # Aceptar cookies si aparecen
        try:
            page.click('button:has-text("Aceptar todo")', timeout=3000)
        except:
            pass

        # Buscar
        search_box = page.locator('input[placeholder="Buscar en Google Maps"]')
        search_box.fill(f"{keyword} {location}")
        search_box.press("Enter")
        time.sleep(5)

        # Extraer resultados
        businesses = []

        # Scroll para cargar más resultados
        for _ in range(3):
            page.evaluate("window.scrollBy(0, 1000)")
            time.sleep(2)

        # Extraer datos del DOM
        results = page.locator("div[role='article']").all()
        for result in results[:20]:  # Primeros 20
            try:
                # Extraer nombre
                name_elem = result.locator('fontHeadline').first
                name = name_elem.inner_text() if name_elem.count() > 0 else ""

                # Extraer valoración
                rating_elem = result.locator('span[aria-label*="estrella"]').first
                rating_text = rating_elem.get_attribute("aria-label") if rating_elem.count() > 0 else "0"

                # Verificar si tiene sitio web
                has_website = bool(result.locator('a[data-tooltip="Sitio web"]').count())

                # Extraer teléfono si está disponible
                phone_elem = result.locator('button[aria-label*="Teléfono"]').first
                # Nota: Requiere hacer click para ver el teléfono completo

                businesses.append({
                    "nombre": name,
                    "valoracion": rating_text,
                    "tiene_web": has_website,
                    "categoria": keyword,
                    "ubicacion": location
                })
            except Exception as e:
                continue

        browser.close()
        return businesses


# Uso para España
if __name__ == "__main__":
    # Nichos de alto margen en España
    keywords_espana = [
        "instalador aire acondicionado",
        "fontanero",
        "electricista",
        "reformas cocina",
        "reformas baño",
        "instalador placas solares",
        "cerrajero",
        "carpintero",
    ]

    locations_espana = [
        "Barcelona",
        "Hospitalet de Llobregat",
        "Badalona",
        "Sabadell",
        "Terrassa",
        "Mataró",
    ]

    # Ejemplo de búsqueda
    negocios = scrape_google_maps_playwright(
        keyword="instalador aire acondicionado",
        location="Barcelona"
    )

    print(f"Encontrados: {len(negocios)} negocios")
    print(json.dumps(negocios[:3], indent=2, ensure_ascii=False))
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
- Proxy residencial: 3-4€ por GB
- Para 10.000 búsquedas: ~40-80€ en proxies

---

## Nichos de Alto Margen en España

### Top 15 Categorías por Margen de Beneficio (España 2025)

| Rank | Categoría | Margen Estimado | Ticket Medio (€) | Ticket Web Anual (€) |
|------|-----------|-----------------|------------------|---------------------|
| 1 | **Reformas Integrales** | 15-25% | 15.000-40.000 | **2.400-3.600** |
| 2 | **Instalación Aire Acondicionado** | 15-25% | 2.500-6.000 | **2.400** |
| 3 | **Fontanería** | 15-20% | 800-3.000 | **2.400** |
| 4 | **Electricidad** | 15-25% | 500-4.000 | **2.400** |
| 5 | **Placas Solares** | 10-20% | 4.500-8.500 | **2.400** |
| 6 | **Carpintería Aluminio/PVC** | 20-30% | 3.000-15.000 | **2.400** |
| 7 | **Cerrajería** | 30-50% | 150-500 | **2.400** |
| 8 | **Pintura y Decoración** | 20-30% | 1.500-5.000 | **2.400** |
| 9 | **Reformas de Baño** | 15-20% | 4.000-8.000 | **2.400** |
| 10 | **Reformas de Cocina** | 15-20% | 8.000-15.000 | **2.400** |
| 11 | **Jardinería y Paisajismo** | 15-20% | 1.500-8.000 | **2.400** |
| 12 | **Limpieza de Fachadas** | 25-35% | 800-2.500 | **2.400** |
| 13 | **Montaje de Muebles** | 20-30% | 300-1.500 | **2.400** |
| 14 | **Reparación de Electrodomésticos** | 25-40% | 150-400 | **2.400** |
| 15 | **Tratamientos de Humedades** | 25-35% | 1.000-5.000 | **2.400** |

### Análisis Detallado por Nicho

#### 1. Reformas Integrales (Cocina/Baño)

```
Ticket medio en Barcelona: 12.000€ - 25.000€
Margen del empresario: 15-25%

Datos de mercado Barcelona:
├── Reforma cocina: 8.000€ - 15.000€ (800-1.100€/m²)
├── Reforma baño: 4.000€ - 8.000€ (650-750€/m²)
├── Reforma integral piso: 800€ - 1.100€/m²
└── Periodo high-season: Septiembre - Diciembre

Características del nicho:
✓ Ticket alto (mínimo 8.000€)
✓ Clientes dispuestos a pagar por calidad
✓ Muchos autónomos sin web profesional
✓ Competencia fragmentada
✓ Buena valoración media en Google Maps (4+★)
```

#### 2. Instalación de Aire Acondicionado

```
Ticket medio en Barcelona: 2.500€ - 6.000€
Margen del empresario: 15-25%

Precios en Barcelona 2025:
├── Instalación básica: 361€ - 610€ (mano de obra)
├── Instalación split: 990€ - 1.500€
├── Instalación con conductos: desde 990€
└── Season alta: Mayo - Septiembre

Características del nicho:
✓ Servicio esencial (calor en España)
✓ Temporada alta muy marcada
✓ Urgencias pagan premium
✓ Muchos pequeños instaladores sin web
✓ Mercado en crecimiento (cambio climático)
```

#### 3. Fontanería

```
Ticket medio: 800€ - 3.000€
Margen del empresario: 15-20%

Servicios comunes:
├── Reparación de fugas: 200€ - 600€
├── Cambio de caldera: 2.000€ - 4.000€
├── Instalación sanitarios: 800€ - 1.500€
├── Desatascos: 150€ - 400€ (urgencia)

Características:
✓ Urgencias pagan más
✓ Servicios recurrentes (mantenimiento)
✓ Muchos fontaneros autónomos
✓ Necesidad de confianza (reseñas importantes)
```

#### 4. Placas Solares (Autoconsumo)

```
Ticket medio en Barcelona: 4.500€ - 8.500€
Margen del instalador: 10-20%

Precios por potencia:
├── 2 kWp: 3.200€ - 4.200€ (1.600-2.100€/kW)
├── 3 kWp: 4.500€ - 5.500€ (1.500-1.833€/kW)
├── 5 kWp: 5.000€ - 6.000€ (1.000-1.200€/kW)
└── 10 kWp: 7.300€ - 8.500€ (730-850€/kW)

Ayudas disponibles en España:
├── Deducción IRPF: 60% (máx. 7.500€/año)
├── IBC Cataluña: Ayudas específicas
└── Next Generation EU: Fondos disponibles

Características:
✓ Mercado en boom (energías renovables)
✓ Ahorro visible para cliente (40-60% factura)
✓ Periodo amortización: 4-7 años
✓ Instaladores nuevos sin web establecida
```

### Palabras Clave para Google Maps por Categoría (España)

```python
# Nichos de ALTO MARGEN en España
HIGH_MARGIN_KEYWORDS_ESPANA = [
    # Muy Alto Margen (+25%)
    "cerrajero",
    "reparacion electrodomesticos",
    "tratamiento humedades",
    "limpieza fachadas",

    # Alto Margen (20-25%)
    "carpintero aluminio",
    "pintor decorator",
    "montaje muebles",

    # Buen Margen con Ticket Alto (15-25%)
    "reformas cocina",
    "reformas baño",
    "reformas integrales",

    # Buen Margen (15-20%)
    "instalador aire acondicionado",
    "fontanero",
    "electricista",
    "jardinero",
    "instalador placas solares",
]

# Ubicaciones Objetivo (por renta per cápita)
HIGH_VALUE_LOCATIONS_ESPANA = [
    # Barcelona y área metropolitana
    "Barcelona",
    "L'Hospitalet de Llobregat",
    "Badalona",
    "Sabadell",
    "Terrassa",
    "Mataró",
    "Granollers",
    "Sant Cugat del Vallès",

    # Otras ciudades de alto valor
    "Madrid",
    "Valencia",
    "Sevilla",
    "Zaragoza",
    "Málaga",
    "Bilbao",
    "Alicante",
]

# Combinación recomendada para empezar
NICHO_PRINCIPAL = {
    "keyword": "reformas integrales",
    "location": "Barcelona",
    "razon": "Ticket medio alto (15K€) + mucha competencia fragmentada"
}
```

### Bases de Datos Enfocadas por Categoría

```
ALTA PRIORIDAD (Margen Alto + Ticket Alto):
├── Reformas Integrales (Cocina/Baño)
├── Instalación Aire Acondicionado
├── Placas Solares
├── Carpintería Aluminio/PVC
└── Tratamiento de Humedades

PRIORIDAD MEDIA (Buen Margen + Buen Ticket):
├── Fontaneros
├── Electricistas
├── Pintores
├── Jardinería
└── Limpieza de Fachadas

PRIORIDAD BAJA (Volumen Alto + Ticket Bajo):
├── Cerrajeros (urgencias)
├── Reparación Electrodomésticos
├── Montaje de Muebles
└── Limpieza Doméstica
```

---

## Análisis Costo-Beneficio (España)

### Escenario 1: Usando API Pagada (Serper.dev/Scrapingdog)

```
Costos mensuales:
├── API (10.000 búsquedas): 37€
├── Claude API (generación sitios): 18€
├── Twilio (500 SMS): ~23€
├── GitHub Pages: 0€
└── Total: ~78€/mes

Métricas:
├── Prospectos contactados: 500/mes
├── Tasa respuesta: 20% = 100 respuestas
├── Tasa conversión: 10% = 10 clientes
├── Ingreso: 10 × 2.400€ = 24.000€/año = 2.000€/mes
├── Costo/adquisición: 78€ ÷ 10 = 7,80€
└── ROI: 2.464%

Conclusión: ✓✓ Muy viable en España
```

### Escenario 2: Scraper Propio con Playwright + Proxies

```
Costo mensual:
├── Desarrollo propio: 0€ (tu tiempo)
├── Proxies residenciales: 40-80€/mes (para volumen)
├── Servidor VPS: 8-12€/mes (opcional)
├── Twilio SMS: 23€/500 SMS
└── Total: ~71-115€/mes

Métricas:
├── Prospectos ilimitados
├── Sin costo por búsqueda
├── Mantenimiento: 2-4 horas/mes
└── Escala infinitamente

Conclusión: ✓✓ Mejor opción a largo plazo
```

### Escenario 3: Híbrido (Recomendado)

```
Fase 1 (Mes 1-2): Usar API con plan gratuito
├── Serper.dev: 2.500 búsquedas gratis
├── Enfocarse en 1-2 categorías
├── Validar el modelo en España
└── Costo: 0€

Fase 2 (Mes 3-6): API pagada o scraper propio
├── Si funciona: Migrar a Playwright + Proxies (71-115€/mes)
├── Si no tiene tiempo: API pagada (78€/mes)
└── Escalar a 10.000+ búsquedas/mes

Conclusión: ✓✓ Mejor balance riesgo/recompensa
```

---

## Plan de Acción para Barcelona

### Estrategia por Semanas

#### Semana 1-2: Validación con API Gratuita

```python
# Paso 1: Obtener créditos gratis
APIs_CREDITOS_GRATIS = {
    "Serper.dev": 2500,  # Créditos al registrarte
    "Scrapingdog": 1000,  # Créditos/mes
    "Total": 3500  # Búsquedas totales
}

# Paso 2: Nichos objetivo en Barcelona
NICHO_BARCELONA = {
    "principal": "Reformas integrales",
    "secundarios": [
        "Aire acondicionado",
        "Fontaneros",
        "Electricistas",
        "Placas solares"
    ],
    "ubicaciones": [
        "Barcelona ciudad",
        "L'Hospitalet",
        "Badalona",
        "Sabadell",
        "Terrassa"
    ]
}

# Paso 3: Ejecutar búsqueda
python src/scraper/api_scraper.py \
    --api serper \
    --keyword "reformas integrales" \
    --location "Barcelona" \
    --language es

# Resultado esperado:
# ~200-300 prospectos calificados
# ~50-100 sin website
# 5-10 demos creadas
# 1-3 conversiones (2.400-7.200€)
```

#### Semana 3-4: Análisis y Optimización

```
1. Analizar resultados de la primera semana
2. Identificar nichos con mejor respuesta
3. Optimizar mensaje y plantillas de SMS/email
4. Ajustar precios según el mercado español

Métricas a monitorear:
├── Tasa de apertura de SMS
├── Tasa de respuesta
├── Tasa de conversión por nicho
├── Ticket medio por cliente
└── Costo de adquisición (CAC)
```

#### Mes 2-3: Escala Decision

```
Si conversión > 5%:
    → Invertir en Playwright + proxies (71-115€/mes)
    → Escalar a todas las categorías de alto margen
    → Contratar ayudante para gestión de clientes
    → Objetivo: 30-50 conversiones/mes (72.000-120.000€/año)

Si conversión < 5%:
    → Optimizar el mensaje y la demo
    → Probar diferentes categorías
    → Mantener API pagada (78€/mes)
    → Enfocarse en nichos específicos
```

### Presupuesto por Fase (Euros)

```
MES 1: 0€ (créditos gratis)
├── APIs: Gratis (Serper.dev + Scrapingdog)
├── Desarrollo: Tu tiempo
├── Hosting demo: Gratis (GitHub Pages/Vercel)
└── Dominio temporal: Gratis (subdominio)

MES 2-3: 78-115€/mes
├── API: 37€/mes (Scrapingdog) o 40-80€ (proxies)
├── Mensajería: 23€/500 SMS
├── Claude: 18€/mes
└── Dominio: 10-15€/año (opcional)

MES 4+: 71-115€/mes (si escala)
├── Proxies: 40-80€
├── Servidor: 8-12€
├── Mensajería: 23€
└── Claude: 18€
```

### Plan de Precios para España

```
PLAN MENSUAL:
├── Precio: 199€/mes (vs 299€ en USA)
├── Incluye: Hosting, dominio, soporte
├── Mantenimiento: Actualizaciones, backups
└── Objetivo: Accesible para autónomos españoles

PLAN ANUAL:
├── Precio: 2.000€/año (vs 3.000€ en USA)
├── Descuento: ~17% vs mensual (2 meses gratis)
├── Incluye: Todo lo mensual + prioritario
└── Objetivo: Flujo de caja predecible

POR QUÉ ESTOS PRECIOS:
├── Salario medio autónomo España: 1.800-2.500€/mes
├── Un cliente = 8-10% del salario mensual
├── ROI positivo con 1 cliente/año
└── Competitivo con agencias web españolas (3K-5K)
```

---

## Recomendaciones Finales

### Por Etapa del Proyecto

#### Etapa 1: Prototipo (Semana 1-2)
**Usar: Serper.dev**
- 2.500 búsquedas gratis
- Validar que el modelo funciona en España
- Probar 1-2 categorías (reformas + aire acondicionado)
- Sin coste inicial

#### Etapa 2: MVP (Mes 1-3)
**Usar: Scrapingdog o Playwright**

| Opción | Cuándo Elegirla |
|--------|-----------------|
| **Scrapingdog** | Tienes presupuesto, quieres rapidez, no quieres mantener código |
| **Playwright** | Tienes tiempo, quieres escalar, prefieres control total |

#### Etapa 3: Producción (Mes 3+)
**Usar: Playwright + Proxies Rotativos**

```python
# Arquitectura recomendada para producción España
┌─────────────────────────────────────────────────────────┐
│              SISTEMA DE PRODUCCIÓN ESPAÑA                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐  │
│  │  PLAYWRIGHT  │───▶│  PROXIES     │───▶│  DATA    │  │
│  │  SCRAPER     │    │  ROTATIVOS   │    │  CLEANER │  │
│  │  (ES Locale) │    │  (EU Nodes)  │    │  (ES)    │  │
│  └──────────────┘    └──────────────┘    └──────────┘  │
│         │                                      │        │
│         ▼                                      ▼        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐  │
│  │  RATE LIMIT  │    │  ERROR       │    │  CSV/DB  │  │
│  │  HANDLER     │    │  RECOVERY    │    │  EXPORT  │  │
│  └──────────────┘    └──────────────┘    └──────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘

Coste mensual: 71-115€ (proxies + hosting)
Capacidad: Ilimitada
Enfoque: España + Barcelona
```

### Tabla de Decisión Rápida

| Tu Situación | Recomendación |
|--------------|---------------|
| Solo quiero probar | Serper.dev (gratis) |
| Tengo 40-80€/mes presupuesto | Scrapingdog API |
| Quiero escalar ilimitadamente | Playwright + proxies |
| No quiero mantener código | Outscraper API |
| Tengo tiempo pero no dinero | Playwright solo |
| Quiero empezar YA | Serper.dev → migrar después |

### Nichos Recomendados para Empezar (España)

```
Fase 1 - Validación (Mes 1):
┌─────────────────────────────────────┐
│ 1. Reformas Integrales (Barcelona)  │ ← Ticket más alto
│ 2. Aire Acondicionado (Barcelona)   │ ← Temporada alta
└─────────────────────────────────────┘

Fase 2 - Expansión (Mes 2-3):
┌─────────────────────────────────────┐
│ 3. Fontaneros (Barcelona + AMC*)    │
│ 4. Placas Solares (Cataluña)        │ ← Mercado en boom
│ 5. Electricistas (AMC*)             │
└─────────────────────────────────────┘

Fase 3 - Escala (Mes 4+):
┌─────────────────────────────────────┐
│ 6. Todas las categorías de alto     │
│    margen en España                 │
│ 7. Expansión a Madrid, Valencia...  │
└─────────────────────────────────────┘

*AMC = Área Metropolitana de Barcelona
```

---

## Fuentes Consultadas

### APIs y Scraping
- [5 Best Google Maps Scraper APIs: Tested & Ranked - ScrapingDog](https://www.scrapingdog.com/blog/best-google-maps-scraper/)
- [Google Maps Scraper Examples (Python & Node.js) - GitHub HasData](https://github.com/HasData/google-maps-scraper)
- [Google SERP API - Free Tier - Outscraper](https://outscraper.com/google-serp-api/)
- [ScraperAPI Pricing - Free 1,000 credits/month](https://www.scraperapi.com/pricing/)
- [Zenserp API Pricing - Affordable Search APIs](https://zenserp.com/pricing-plans/)

### Librerías Python
- [How to Scrape Google Maps Data with Python - Medium](https://medium.com/@datajournal/how-to-scrape-google-maps-with-python-510dbcca4e92)
- [Google Maps Scraper Examples (Python & Node.js)](https://github.com/HasData/google-maps-scraper)

### Mercado España y Barcelona
- [Cristian, dueño de negocio de reformas: "Hoy en día un buen albañil debería estar ganando 2.800€ al mes" - El Español](https://www.elespanol.com/sociedad/20251231/cristian-dueno-negocio-reformas-hoy-dia-espana-buen-albanil-deberia-ganando-mes/1003744074481_0.html)
- [Sueldo Jefe de Obra España 2025: Salarios por Experiencia - Jefe de Obra Pro](https://jefedeobra.pro/blog/sueldo-jefe-obra-espana-2025)
- [Precio mano de obra construcción 2025 - AutoPromotor](https://autopromotor.info/constructoras/precio-mano-de-obra-construccion/)
- [Top sueldos en construcción y real estate 2025 - Obras Urbanas](https://obrasurbanas.es/profesiones-mejor-pagadas-construccion-real-estate-2025-lhh/)
- [Convenio Colectivo de la Construcción 2025 - Skello](https://www.skello.es/blog/todo-lo-que-necesitas-saber-sobre-el-convenio-del-sector-de-la-construccion-2024)
- [Las pymes catalanas aumentaron sus beneficios el triple que los salarios - El Periódico](https://www.elperiodico.com/es/economia/20250917/pymes-catalanas-aumentaron-beneficios-triple-salarios-2023-anuario-pimec-121663030)
- [La Cámara cierra el 2025 con un beneficio de 1 M€ - Ara](https://es.ara.cat/economia/patronales/camara-cierra-2025-beneficio-1-m-aumenta-presupuesto-2026-34-m_1_5597554.html)

### Precios Reformas Barcelona
- [Cuánto Puede Costar una Reforma en Barcelona - Instalaciones Expósito](https://www.instalacionesexposito.com/cuanto-puede-costar-una-reforma-en-barcelona/)
- [¿Cuánto cuesta la reforma integral de un piso en Barcelona? - Bysincro](https://www.bysincro.com/cuanto-cuesta-reforma-integral-barcelona/)
- [Cuánto cuesta reformar una cocina en Barcelona - 1Reformas](https://1reformas.com/cuanto-cuesta-reformar-una-cocina/)
- [Coste Reforma de Cocina 2025: Precios por Ciudades - Wolly](https://www.wollyhome.com/blog/guia-definitiva-como-reformar-tu-cocina-en-2025)

### Precios Servicios Barcelona
- [Instaladores de aire acondicionado Barcelona - CaloryFrio](https://presupuestos.caloryfrio.com/instaladores-aire-acondicionado-barcelona.html)
- [Instalación Aire Acondicionado en Barcelona - Cronoshare](https://www.cronoshare.com/servicios/presupuesto-instalacion-aire-acondicionado/barcelona/barcelona)
- [Precio fontanero en Barcelona - Planreforma](https://planreforma.com/presupuestos-para-barcelona-barcelona-fontanero/)
- [Estrada Servicios: Fontanero, Electricista y Gas en Barcelona](https://estradaservicios.com/)

### Precios Placas Solares
- [¿Cuánto cuesta instalar placas solares en Barcelona? - Cronoshare](https://www.cronoshare.com/cuanto-cuesta/instalar-placas-solares/barcelona)
- [Precio por instalar placas solares en España en 2025 - Solfy](https://solfy.net/autoconsumo/placas-solares/precio/)
- [¿Cuánto cuesta instalar placas solares? Precios en 2025 - Habitissimo](https://www.habitissimo.es/presupuestos/placas-solares)
- [Precio instalación placas solares 2025 - AutoSolar](https://autosolar.es/mi-experiencia-placas-solares/cuanto-cuesta-una-instalacion-fotovoltaica)
- [Placas solares Barcelona: Precio, ayudas, ahorro - SFE Solar](https://www.sfe-solar.com/instalaciones-fotovoltaicas/instalacion/empresas/barcelona/)

---

**Documento creado:** 2025-01-02
**Última actualización:** 2025-01-02
**Próxima revisión recomendada:** Cada 3 meses (precios cambian)
