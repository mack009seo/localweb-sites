#!/usr/bin/env python3
import csv
import os
import json
import re
import shutil
import hashlib
import urllib.parse
from datetime import datetime
from src.generator.blog_generator import BlogGenerator

class StaticSiteGenerator:
    """Genera aterrizajes premium de una sola página para prospectos"""

    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.template_dir = "templates/site"
        # Mapeo de categorías a imágenes generadas
        self.category_images = {
            "carpintero aluminio": ["carpenter_aluminium_1.png", "carpenter_aluminium_2.png", "carpenter_aluminium_3.png"],
            "electricista": ["electrician_1.png", "electrician_2.png", "electrician_3.png"],
            "pintor": ["painter_1.png", "painter_2.png", "painter_3.png"],
            "jardinero": ["gardener_1.png", "gardener_2.png", "gardener_3.png"],
            "fontanero": ["plumber_1.png", "plumber_2.png", "plumber_3.png"],
            "cerrajero": ["locksmith_1.png", "locksmith_2.png", "locksmith_3.png"],
            "aire acondicionado": ["ac_1.png", "ac_2.png", "ac_3.png"],
            "placas solares": ["solar_1.png", "solar_2.png", "solar_3.png"],
            "limpieza": ["cleaning_1.png", "cleaning_2.png", "cleaning_3.png"],
            "reformas": ["renovation_1.png", "renovation_2.png", "renovation_3.png"],
            "default": ["default_1.png", "default_2.png", "default_3.png"]
        }
        # Ahora usamos una ruta local relativa para los assets
        self.assets_dir = os.path.join(os.getcwd(), "assets/hero_images")
        self.blog_gen = BlogGenerator()
        
        # Mapeo para Schema.org SEO
        self.schema_map = {
            "electricista": "Electrician",
            "pintor": "PaintingService",
            "fontanero": "PlumbingService",
            "cerrajero": "Locksmith",
            "jardinero": "GardenStore",
            "aire acondicionado": "HVACBusiness",
            "carpintero": "HomeAndConstructionBusiness",
            "reformas": "GeneralContractor",
            "limpieza": "CleaningService",
            "default": "LocalBusiness"
        }

    def _slugify(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_-]+', '-', text)
        return text.strip('-')

    def _get_hero_image(self, category: str) -> str:
        category = category.lower()
        import random
        for key in self.category_images:
            if key in category:
                images = self.category_images[key]
                return random.choice(images) if isinstance(images, list) else images
        
        defaults = self.category_images["default"]
        return random.choice(defaults) if isinstance(defaults, list) else defaults

    def _get_schema_type(self, category: str) -> str:
        category = category.lower()
        for key in self.schema_map:
            if key in category:
                return self.schema_map[key]
        return self.schema_map["default"]
    
    def _get_service_cards(self, category: str) -> str:
        """Genera HTML de cartas de servicio específicas para la categoría"""
        cat = category.lower()
        
        services = {
            "electricista": [
                ("Urgencias 24h", "Atención inmediata para averías críticas, cortocircuitos y apagones."),
                ("Boletines e Informes", "Certificados de instalación eléctrica y aumentos de potencia oficiales."),
                ("Instalaciones Nuevas", "Reformas eléctricas completas y cuadros de protección modernos.")
            ],
            "pintor": [
                ("Pintura de Interiores", "Acabados impecables con pinturas de alta calidad y limpieza total."),
                ("Alisado de Paredes", "Eliminación de gotelé y preparación de superficies para un acabado moderno."),
                ("Tratamiento de Humedades", "Soluciones definitivas contra manchas y filtraciones con productos técnicos.")
            ],
            "carpintero aluminio": [
                ("Ventanas y Cerramientos", "Máximo aislamiento térmico y acústico con perfiles de alta gama."),
                ("Persianas y Motores", "Instalación, reparación y motorización de persianas para tu comodidad."),
                ("Puertas y Mamparas", "Diseños a medida en aluminio y vidrio para baños y entradas.")
            ],
            "reformas": [
                ("Reformas Integrales", "Gestión completa de tu proyecto de reforma con los mejores profesionales."),
                ("Cocinas y Baños", "Modernización de espacios con materiales premium y diseño funcional."),
                ("Gestión de Licencias", "Nos encargamos de toda la burocracia para que no te preocupes por nada.")
            ],
            "fontanero": [
                ("Urgencias 24h", "Reparación inmediata de fugas, roturas y desatascos en toda la ciudad."),
                ("Instalaciones Gratuitas", "Sustitución de grifería, sanitarios y sistemas de calefacción con garantía."),
                ("Detección de Fugas", "Tecnología de última generación para localizar averías sin romper paredes.")
            ],
            "cerrajero": [
                ("Apertura de Puertas", "Servicio rápido y sin daños para todo tipo de puertas y cerraduras."),
                ("Cambio de Bombines", "Aumentamos tu seguridad con sistemas antibumping de alta gama."),
                ("Cerraduras Inteligentes", "Instalación de sistemas digitales y control de acceso moderno.")
            ],
            "aire acondicionado": [
                ("Instalación Premium", "Montaje profesional de sistemas Split y conductos de máxima eficiencia."),
                ("Mantenimiento y Carga", "Limpieza de filtros y recarga de gas para un aire puro y eficiente."),
                ("Reparación Express", "Solución rápida a averías mecánicas y electrónicas en tu climatización.")
            ],
            "jardinero": [
                ("Mantenimiento Integral", "Cuidado experto de jardines, poda de árboles y control de plagas."),
                ("Diseño y Paisajismo", "Transformamos tu espacio exterior en un oasis personalizado."),
                ("Riego Automático", "Instalación de sistemas de riego eficientes para ahorrar agua.")
            ],
            "limpieza": [
                ("Limpieza de Fachadas", "Recuperamos el aspecto original de tu edificio con técnicas no agresivas."),
                ("Mantenimiento de Oficinas", "Ambientes de trabajo impecables y desinfectados para tu equipo."),
                ("Limpieza Fin de Obra", "Eliminación total de residuos para que disfrutes de tu espacio de inmediato.")
            ],
            "placas solares": [
                ("Autoconsumo Solar", "Reduce tu factura eléctrica con una instalación fotovoltaica a medida."),
                ("Estudio de Eficiencia", "Análisis gratuito de tu cubierta y potencial de ahorro energético."),
                ("Mantenimiento Solar", "Revisiones periódicas para asegurar el máximo rendimiento de tus paneles.")
            ],
            "default": [
                ("Calidad Garantizada", "Compromiso total con la excelencia en cada trabajo realizado."),
                ("Presupuesto a Medida", "Estudio detallado de tus necesidades sin compromiso alguno."),
                ("Atención Local", "Servicio rápido y cercano en toda el área de Barcelona.")
            ]
        }
        
        selected = services.get("default")
        for key in services:
            if key in cat:
                selected = services[key]
                break
        
        html = ""
        for title, desc in selected:
            html += f"""
                <div class="card">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>"""
        return html

    def _get_trust_badges(self) -> str:
        """Genera HTML para insignias de confianza"""
        badges = [
            ("Presupuesto Gratis", "✓"),
            ("Sin Compromiso", "✓"),
            ("Garantía Calidad", "✓"),
            ("Atención 24h", "✓")
        ]
        
        html = '<div class="trust-badges">'
        for label, icon in badges:
            html += f'<div class="trust-badge"><span class="badge-icon">{icon}</span> {label}</div>'
        html += '</div>'
        return html

    def _get_sticky_footer(self, phone: str, category: str, slug: str, biz_name: str) -> str:
        """Genera el footer pegajoso para móviles"""
        msg = f"Hola {biz_name}, solicito más información sobre vuestros servicios de {category.capitalize()}.\n\n(Enviado desde https://localpro.top/{slug}/)"
        msg_encoded = urllib.parse.quote(msg)
        return f"""
        <div class="sticky-mobile-cta">
            <a href="https://wa.me/{phone}?text={msg_encoded}" class="btn btn-whatsapp">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" width="24">
                ¡Contactar por WhatsApp!
            </a>
        </div>
        """

    def _extract_neighborhood(self, address: str) -> str:
        """Intenta extraer el barrio/distrito de la dirección"""
        if not address:
            return ""
        parts = [p.strip() for p in address.split(',')]
        # El barrio suele estar antes del código postal o la ciudad
        # Ejemplo: "Carrer de los Castillejos, 251, Eixample, 08013 Barcelona"
        # Buscamos la parte que no sea calle, número, CP o ciudad
        for i, part in enumerate(parts):
            if re.search(r'\d{5}', part) or "barcelona" in part.lower():
                if i > 0:
                    return parts[i-1]
        return ""

    def _get_hero_title(self, category: str) -> str:
        """Genera un título H1 adaptado al nicho conservando la esencia de 'la mejor herramienta'"""
        cat = category.lower()
        
        titles = {
            "electricista": "Tu energía en buenas manos, nuestra mejor herramienta.",
            "pintor": "Espacios que inspiran, tu confianza es nuestra mejor herramienta.",
            "carpintero aluminio": "Cerramientos impecables, tu hogar es nuestra mejor herramienta.",
            "reformas": "Transformamos tu visión, tu confianza es nuestra mejor herramienta.",
            "jardinero": "Naturaleza en armonía, tu satisfacción es nuestra mejor herramienta.",
            "aire acondicionado": "Confort en cada rincón, tu bienestar es nuestra mejor herramienta.",
            "limpieza": "Pulcritud garantizada, tu tranquilidad es nuestra mejor herramienta.",
            "placas solares": "Energía del futuro, tu ahorro es nuestra mejor herramienta.",
            "default": "Tu confianza, nuestra mejor herramienta."
        }
        
        for key in titles:
            if key in cat:
                return titles[key]
        return titles["default"]

    def _get_faq_data(self, category: str) -> list:
        """Retorna una lista de preguntas y respuestas según la categoría"""
        cat = category.lower()
        
        faqs = {
            "electricista": [
                {"q": "¿Realizáis servicios de urgencia 24 horas?", "a": "Sí, atendemos urgencias eléctricas las 24 horas del día, los 7 días de la semana, con una respuesta rápida para solucionar cualquier avería."},
                {"q": "¿Tenéis carnet de instalador autorizado?", "a": "Absolutamente. Todos nuestros técnicos son instaladores autorizados y podemos emitir boletines eléctricos oficiales (CIE)."},
                {"q": "¿Qué garantía tienen vuestras reparaciones?", "a": "Todas nuestras intervenciones cuentan con garantía por escrito tanto en mano de obra como en los materiales instalados."}
            ],
            "pintor": [
                {"q": "¿Cuánto tardáis en pintar un piso estándar?", "a": "Para un piso medio, solemos tardar entre 2 y 4 días, dependiendo del estado de las paredes y si hay que alisar gotelé."},
                {"q": "¿Incluís la limpieza después del trabajo?", "a": "Sí, protegemos todo el mobiliario y suelos, y realizamos una limpieza exhaustiva al finalizar para que no tengas que preocuparte de nada."},
                {"q": "¿Asesoráis sobre los colores y tipos de pintura?", "a": "Claro, te ayudamos a elegir la mejor combinación de colores y el tipo de pintura adecuado (lavable, ecológica, etc.) para cada estancia."}
            ],
            "carpintero aluminio": [
                {"q": "¿Qué ventajas tiene el PVC frente al aluminio?", "a": "El PVC suele ofrecer un aislamiento térmico ligeramente superior, mientras que el aluminio destaca por su resistencia técnica y perfiles más finos."},
                {"q": "¿Hacéis presupuestos sin compromiso?", "a": "Sí, nos desplazamos a tu domicilio para tomar medidas y darte un presupuesto detallado sin coste alguno."},
                {"q": "¿Instaláis persianas motorizadas?", "a": "Instalamos todo tipo de persianas, incluyendo sistemas de motorización compatibles con domótica."}
            ],
            "reformas": [
                {"q": "¿Os encargáis de la gestión de licencias?", "a": "Nos encargamos de toda la gestión administrativa y técnica para solicitar los permisos de obra necesarios."},
                {"q": "¿Cómo se estructuran los pagos de la reforma?", "a": "Trabajamos con un calendario de pagos por hitos finalizados, para que siempre veas el progreso antes de cada abono."},
                {"q": "¿Tenéis seguro de responsabilidad civil?", "a": "Sí, contamos con un seguro de responsabilidad civil completo para cubrir cualquier imprevisto durante la ejecución."}
            ],
            "fontanero": [
                {"q": "¿Atendéis urgencias de fontanería?", "a": "Sí, estamos disponibles las 24 horas para desatascos, roturas de tuberías y cualquier emergencia que requiera atención inmediata."},
                {"q": "¿Hacéis instalaciones de gas?", "a": "Contamos con técnicos autorizados para realizar boletines de gas, instalaciones y reparaciones cumpliendo toda la normativa vigente."},
                {"q": "¿Cómo detectáis las fugas de agua?", "a": "Utilizamos geófonos y cámaras térmicas para localizar el punto exacto de la fuga sin necesidad de picar paredes innecesariamente."}
            ],
            "cerrajero": [
                {"q": "¿Cuánto tardáis en llegar?", "a": "En servicios de urgencia, solemos llegar en menos de 20-30 minutos en cualquier punto de Barcelona y alrededores."},
                {"q": "¿Abrís puertas sin romper la cerradura?", "a": "Nuestra prioridad es la apertura limpia. En el 90% de los casos abrimos sin causar daños estéticos o estructurales a la puerta."},
                {"q": "¿Instaláis cerraduras de alta seguridad?", "a": "Sí, somos expertos en sistemas antibumping, escudos acorazados y cerrojos suplementarios para maximizar tu protección."}
            ],
            "aire acondicionado": [
                {"q": "¿Cuándo es mejor hacer el mantenimiento?", "a": "Recomendamos una revisión a fondo antes de que empiece el verano para asegurar que el sistema rinde al máximo y el aire es puro."},
                {"q": "¿Qué marcas instaláis?", "a": "Trabajamos con las mejores marcas del mercado (Daikin, Mitsubishi, Fujitsu, Panasonic) ofreciendo garantía oficial en todas ellas."},
                {"q": "¿Incluís la carga de gas?", "a": "Sí, realizamos comprobaciones de fugas y recargas de gas refrigerante para que tu equipo vuelva a enfriar como el primer día."}
            ],
            "limpieza": [
                {"q": "¿Qué productos utilizáis para la limpieza?", "a": "Utilizamos productos biodegradables y certificados, garantizando la desinfección total sin dañar superficies ni el medio ambiente."},
                {"q": "¿Hacéis limpiezas fin de obra?", "a": "Sí, somos expertos en dejar espacios perfectos tras una reforma, eliminando polvo, restos de silicona y manchas difíciles."},
                {"q": "¿Tenéis personal asegurado?", "a": "Todo nuestro equipo está debidamente asegurado y cumplimos estrictamente con la normativa de prevención de riesgos laborales."}
            ],
            "jardinero": [
                {"q": "¿Hacéis servicios de poda?", "a": "Realizamos podas de formación, mantenimiento y limpieza, así como podas en altura con total seguridad."},
                {"q": "¿Instaláis sistemas de riego?", "a": "Diseñamos e instalamos sistemas de riego automático eficientes para optimizar el consumo de agua en tu jardín."},
                {"q": "¿Tratáis plagas en plantas?", "a": "Sí, aplicamos tratamientos fitosanitarios específicos para proteger tus plantas de las plagas más comunes en Barcelona."}
            ],
            "placas solares": [
                {"q": "¿Qué ahorro puedo esperar?", "a": "Dependiendo de tu consumo y ubicación, puedes reducir tu factura eléctrica entre un 50% y un 70% desde el primer mes."},
                {"q": "¿Hay subvenciones disponibles?", "a": "Te asesoramos y gestionamos todas las ayudas actuales (Next Generation, bonificaciones de IBI) para que tu inversión se amortice antes."},
                {"q": "¿Qué mantenimiento requieren?", "a": "Las placas solares son muy duraderas. Solo requieren una limpieza periódica y una revisión anual del inversor y las conexiones."}
            ],
            "default": [
                {"q": "¿Ofrecéis presupuesto gratuito?", "a": "Sí, facilitamos presupuestos detallados y personalizados sin compromiso tras evaluar tus necesidades."},
                {"q": "¿Qué tiempo de garantía ofrecéis?", "a": "Ofrecemos garantía profesional en todos nuestros servicios y materiales, asegurando tu total satisfacción."},
                {"q": "¿Tenéis referencias de trabajos anteriores?", "a": "Contamos con una amplia cartera de clientes satisfechos y podemos mostrarte ejemplos de proyectos similares al tuyo."}
            ]
        }
        
        for key in faqs:
            if key in cat:
                return faqs[key]
        return faqs["default"]

    def _get_faq_html(self, faq_data: list) -> str:
        """Convierte los datos de FAQ en HTML"""
        html = '<div class="faq-grid">'
        for item in faq_data:
            html += f"""
            <div class="faq-item">
                <h3>{item['q']}</h3>
                <p>{item['a']}</p>
            </div>
            """
        html += '</div>'
        return html

    def _generate_sitemap(self, slug: str, site_dir: str):
        """Genera un sitemap.xml básico para el sitio"""
        sitemap_template = f"{self.template_dir}/sitemap.xml"
        if not os.path.exists(sitemap_template):
            return
            
        with open(sitemap_template, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Reemplazar placeholders
        content = content.replace("[[BUSINESS_NAME_SLUG]]", slug)
        content = content.replace("[[DATE]]", datetime.now().strftime("%Y-%m-%d"))
        
        with open(f"{site_dir}/sitemap.xml", 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_colors(self, name: str) -> dict:
        """Genera una paleta de colores coherente basada en el nombre."""
        # Usar el hash del nombre para obtener colores consistentes
        hash_val = int(hashlib.md5(name.encode()).hexdigest(), 16)
        
        # Tonos profesionales (azul, verde, gris, naranja oscuro)
        hues = [210, 220, 200, 160, 25, 30] # Blue, Dark Blue, Light Blue, Teal, Orange, Deep Orange
        hue = hues[hash_val % len(hues)]
        
        return {
            '[[PRIMARY_COLOR]]': f'hsl({hue}, 70%, 45%)',
            '[[PRIMARY_HOVER_COLOR]]': f'hsl({hue}, 70%, 35%)',
            '[[ACCENT_COLOR]]': f'hsl({(hue + 180) % 360}, 70%, 50%)'
        }

    def generate_site(self, prospect: dict):
        p_id = prospect.get("prospect_id", "unknown")
        name = prospect.get("nombre", "unknown")
        slug = self._slugify(name)
        site_dir = f"sites/{slug}"
        
        print(f"Generando Landing Page SEO para: {name} ({p_id})")
        
        # 1. Limpiar/Crear estructura
        if os.path.exists(site_dir):
            shutil.rmtree(site_dir)
            
        os.makedirs(f"{site_dir}/assets/css", exist_ok=True)
        os.makedirs(f"{site_dir}/assets/images", exist_ok=True)
        
        # 2. Copiar assets estáticos
        shutil.copy(f"{self.template_dir}/assets/css/style.css", f"{site_dir}/assets/css/style.css")
        
        # 3. Copiar imagen hero personalizada
        hero_filename = self._get_hero_image(prospect.get("categoria", ""))
        src_image = os.path.join(self.assets_dir, hero_filename)
        if os.path.exists(src_image):
            shutil.copy(src_image, f"{site_dir}/assets/images/hero.jpg")
        else:
            print(f"Warning: Image not found {src_image}, using default")
            default_img = os.path.join(self.assets_dir, "default.png")
            if os.path.exists(default_img):
                 shutil.copy(default_img, f"{site_dir}/assets/images/hero.jpg")
        
        # 4. Procesar variables de contacto
        phone = prospect.get("telefono_normalizado", prospect.get("telefono", ""))
        phone_clean = re.sub(r'\D', '', phone)
        if not phone_clean.startswith('34') and len(phone_clean) == 9:
            phone_clean = '34' + phone_clean
            
        # 5. Variables de SEO
        category_raw = prospect.get("categoria", "Servicios Profesionales")
        city = prospect.get("ubicacion", "Barcelona")
        address = prospect.get("direccion", "").replace('"', '').replace("'", "")
        
        # URL de Google Maps para el iframe
        map_query = f"{name} {address} {city}".replace(" ", "+")
        map_url = f"https://www.google.com/maps/embed/v1/place?key=REPLACE_WITH_MAPS_API_KEY&q={map_query}"
        # Como no tenemos API Key, usaremos el formato de búsqueda pública por ahora (iframe sin key)
        map_url = f"https://maps.google.com/maps?q={map_query}&t=&z=13&ie=UTF8&iwloc=&output=embed"

        schema_type = self._get_schema_type(category_raw)
        
        # 6. Procesar index.html (Única página)
        template_path = f"{self.template_dir}/index.html"
        # Extract and process rating / reviews
        try:
            rating = float(prospect.get('valoracion', 0))
            reviews_count = int(prospect.get('num_reseñas', 0))
        except (ValueError, TypeError):
            rating = 0
            reviews_count = 0

        reviews_block = ""
        json_ld_rating = ""
        
        # Condition: more than 5 reviews and rating more than 3
        if reviews_count > 5 and rating > 3:
            # Generate visual stars
            full_stars = int(rating)
            stars_html = "★" * full_stars + "☆" * (5 - full_stars)
            
            reviews_block = f"""
            <div class="rating-badge">
                <span class="stars">{stars_html}</span>
                <span class="rating-value">{rating}</span>
                <span class="reviews-count">({reviews_count} reseñas en Google)</span>
            </div>
            """
            
            json_ld_rating = f"""
            "aggregateRating": {{
                "@type": "AggregateRating",
                "ratingValue": "{rating}",
                "reviewCount": "{reviews_count}"
            }},
            """

        # 5. SEO & Hyper-Local
        neighborhood = self._extract_neighborhood(address)
        seo_city = f"{neighborhood}, {city}" if neighborhood else city
        
        # 6. FAQ Section & Schema
        faq_data = self._get_faq_data(category_raw)
        faq_html = self._get_faq_html(faq_data)
        
        # Generar JSON-LD FAQ
        json_ld_faq = ""
        if faq_data:
            json_ld_faq = f"""
            ,{{
              "@context": "https://schema.org",
              "@type": "FAQPage",
              "mainEntity": [{", ".join([f'{{ "@type": "Question", "name": "{item["q"]}", "acceptedAnswer": {{ "@type": "Answer", "text": "{item["a"]}" }} }}' for item in faq_data])}]
            }}
            """

        replacements = {
            "[[BUSINESS_NAME]]": name.replace('"', '').replace("'", ""),
            "[[CATEGORY]]": category_raw.capitalize(),
            "[[PHONE]]": phone,
            "[[PHONE_CLEAN]]": phone_clean,
            "[[ADDRESS]]": address,
            "[[CITY]]": city,
            "[[NEIGHBORHOOD]]": neighborhood if neighborhood else city,
            "[[SCHEMA_TYPE]]": schema_type,
            "[[MAP_URL]]": map_url,
            "[[SEO_TITLE]]": f"{category_raw.capitalize()} en {seo_city}",
            "[[DYNAMIC_SEO_TITLE]]": f"{category_raw.capitalize()} en {seo_city} | {name}",
            "[[HERO_TITLE]]": self._get_hero_title(category_raw),
            "[[BUSINESS_NAME_SLUG]]": slug,
            "[[YEAR]]": str(datetime.now().year),
            '[[REVIEWS_BLOCK]]': reviews_block,
            '[[JSON_LD_RATING]]': json_ld_rating,
            '[[SERVICE_CARDS]]': self._get_service_cards(category_raw),
            '[[TRUST_BADGES]]': self._get_trust_badges(),
            '[[FAQ_SECTION]]': faq_html,
            '[[JSON_LD_FAQ]]': json_ld_faq,
            '[[STICKY_FOOTER]]': self._get_sticky_footer(phone_clean, category_raw, slug, name)
        }
        
        # 5.5 Generar colores dinámicos
        colors = self._generate_colors(name)
        replacements.update(colors)

        # 5.6 Generar Blog
        blog_posts = self.blog_gen.generate_blog(
            site_dir,
            category_raw,
            name,
            colors['[[PRIMARY_COLOR]]'],
            colors['[[PRIMARY_HOVER_COLOR]]'],
            colors['[[ACCENT_COLOR]]'],
            phone,
            slug
        )
        
        blog_html = ""
        for post in blog_posts:
            blog_html += f"""
            <div class="card" style="display: flex; flex-direction: column;">
                <h3 style="margin-bottom: 10px;">{post['title']}</h3>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 20px;">{post['excerpt']}</p>
                <a href="blog/{post['filename']}" class="btn btn-demo" style="margin-top: auto;">Leer más</a>
            </div>
            """
        replacements['[[BLOG_POSTS]]'] = blog_html

        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for key, value in replacements.items():
            content = content.replace(key, str(value))
            
        # 5.8 Robots.txt & Sitemap
        # robots.txt con reemplazo
        robots_template = f"{self.template_dir}/robots.txt"
        if os.path.exists(robots_template):
            with open(robots_template, 'r', encoding='utf-8') as f:
                robots_content = f.read()
            robots_content = robots_content.replace("[[BUSINESS_NAME_SLUG]]", slug)
            with open(f"{site_dir}/robots.txt", 'w', encoding='utf-8') as f:
                f.write(robots_content)
        self._generate_sitemap(slug, site_dir)

        with open(f"{site_dir}/index.html", 'w', encoding='utf-8') as f:
            f.write(content)
        
        
        print(f"✓ Landing page '{slug}' generada.")
        return slug

    def process_batch(self, limit: int = 5):
        if not os.path.exists(self.csv_file):
            print(f"Error: No se encuentra el archivo {self.csv_file}")
            return []

        generated_data = []
        with open(self.csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if count >= limit:
                    break
                
                # Smart Filter: Solo procesar prospectos en estado 'pending' (o sin columna estado aún)
                estado = row.get('estado', 'pending')
                if estado != 'pending':
                    continue

                slug = self.generate_site(row)
                if slug:
                    generated_data.append((row, slug))
                    count += 1
        
        return generated_data

if __name__ == "__main__":
    generator = StaticSiteGenerator("data/cleaned_prospects_BARCELONA.csv")
    generator.process_batch(limit=5)
