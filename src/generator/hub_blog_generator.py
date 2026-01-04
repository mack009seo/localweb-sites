import os
from datetime import datetime

class HubBlogGenerator:
    """Generates the main B2B blog for the LocalPro Hub."""

    def __init__(self, output_dir="sites/blog", template_path="templates/site/blog_post.html"):
        self.output_dir = output_dir
        # We'll reuse the site blog template but adapt it for the hub
        self.template_path = "templates/directory/blog_post.html" 
        self.articles = [
            {
                "slug": "importancia-web-negocio-local-2026",
                "title": "La Importancia Vital de una Página Web para Negocios Locales en 2026",
                "excerpt": "¿Sigues pensando que el boca a boca es suficiente? Descubre por qué el 85% de los clientes no contratarán tus servicios si no te encuentran en Google.",
                "content": """
                    <h2>La Era de la Confianza Digital</h2>
                    <p>En el panorama comercial actual, la primera impresión ya no ocurre cuando un cliente entra por la puerta de tu tienda o llama a tu teléfono. Ocurre segundos después de buscar "fontanero cerca de mí" o "reformas en Barcelona" en su móvil. Si tu negocio no aparece, o peor aún, si aparece con una ficha incompleta y sin página web, para el consumidor moderno, simplemente <strong>no existes</strong> o no eres de fiar.</p>
                    <p>Tener una página web profesional en 2026 es el equivalente digital a tener un local limpio y bien iluminado. Transmite autoridad, permanencia y profesionalidad. Una web bien diseñada actúa como tu comercial 24/7, respondiendo preguntas frecuentes, mostrando tu portafolio de trabajos y recogiendo datos de contacto incluso mientras duermes.</p>

                    <h2>Más Allá de las Redes Sociales</h2>
                    <p>Muchos autónomos caen en la trampa de pensar que una página de Facebook o un perfil de Instagram son suficientes. El problema es que en las redes sociales, tú no eres el dueño de tu audiencia; el algoritmo lo es. Un cambio en las políticas de visibilidad puede hacer desaparecer tu negocio de la noche a la mañana. Tu página web, en cambio, es tu territorio propio, tu activo digital. Es el centro neurálgico donde tú controlas el mensaje, la imagen y la experiencia del usuario sin distracciones de la competencia.</p>
                    
                    <h2>Credibilidad y Cierre de Ventas</h2>
                    <p>Imagina dos electricistas con el mismo precio. El primero te envía un presupuesto por WhatsApp y no encuentras nada sobre él en internet. El segundo tiene una web donde puedes ver fotos de sus instalaciones anteriores, leer testimonios reales de vecinos y verificar sus certificaciones. ¿A quién elegirías? La web elimina la fricción de la desconfianza, facilitando que el cliente tome la decisión de compra mucho más rápido.</p>
                """ # Extended content would go here
            },
            {
                "slug": "como-aparecer-primero-google-seo-local",
                "title": "SEO Local: Cómo Hacer que tu Negocio Aparezca Primero en Google Maps",
                "excerpt": "Aparecer en el 'Pack Local' de Google puede duplicar tus llamadas de la noche a la mañana. Te explicamos los factores clave de posicionamiento.",
                "content": """
                    <h2>¿Qué es el SEO Local y por qué es crucial?</h2>
                    <p>El SEO local es el conjunto de estrategias diseñadas para posicionar tu negocio en las búsquedas geolocalizadas. Cuando alguien busca "pintores en [Tu Ciudad]", Google prioriza los resultados más cercanos y relevantes. Estar en los tres primeros resultados de Google Maps (el famoso 'Local Pack') asegura que te lleves más del 60% de los clics de usuarios con intención de compra inmediata.</p>
                    
                    <h2>Factores de Ranking Fundamentales</h2>
                    <p>Google utiliza tres pilares para decidir quién sale primero: Proximidad, Relevancia y Prominencia. Mientras que no puedes cambiar dónde está físicamente tu cliente (Proximidad), sí puedes optimizar los otros dos. La <strong>Relevancia</strong> se mejora teniendo una página web que describa detalladamente tus servicios utilizando las mismas palabras clave que usan tus clientes. La <strong>Prominencia</strong> se construye a través de reseñas positivas constantes y citaciones en directorios locales de calidad.</p>
                    
                    <h2>La Sinergia entre tu Web y Google Business Profile</h2>
                    <p>Tu ficha de Google Business Profile (antes Google My Business) y tu página web deben hablar el mismo idioma. Tener una web optimizada con datos estructurados (Schema.org) ayuda a Google a entender exactamente qué haces y dónde prestas servicio, reforzando la autoridad de tu ficha de mapas. Sin una web sólida que respalde tu ficha, es muy difícil competir con negocios que sí la tienen por las primeras posiciones.</p>
                """
            },
            {
                "slug": "ventajas-web-profesional-vs-hazlo-tu-mismo",
                "title": "Web Profesional vs. DIY: Por qué lo Barato Sale Caro",
                "excerpt": "Analizamos las diferencias de rendimiento, seguridad y conversión entre una web hecha por un experto y una plantilla gratuita.",
                "content": """
                    <h2>El Mito del 'Hazlo Tú Mismo' en Web</h2>
                    <p>Plataformas como Wix o Squarespace prometen webs "en 5 minutos". Pero la realidad es que el diseño web es una disciplina que combina psicología de venta, ingeniería técnica y diseño gráfico. Una web hecha por un aficionado suele cargar lento, verse mal en móviles y carecer de una estructura lógica de conversión. Al final, tienes una web "bonita" que no vende.</p>
                    
                    <h2>Velocidad de Carga y Core Web Vitals</h2>
                    <p>Google penaliza severamente las webs lentas. Un sitio profesional está optimizado a nivel de código para cargar en menos de 2 segundos. Las herramientas gratuitas suelen inyectar tanto código basura que lastran el rendimiento, haciendo que los usuarios abandonen antes de ver tu oferta. En LocalPro, cada línea de código está pensada para la velocidad.</p>
                    
                    <h2>Seguridad y Mantenimiento</h2>
                    <p>Una web desactualizada es un coladero para hackers. Los servicios profesionales incluyen mantenimiento técnico, copias de seguridad y certificados SSL avanzados que protegen los datos de tus clientes. Dormir tranquilo sabiendo que tu negocio digital está blindado es una ventaja que las soluciones gratuitas no pueden ofrecer.</p>
                """
            },
            {
                "slug": "digitalizar-negocio-tradicional-paso-a-paso",
                "title": "De la Libreta a la Nube: Digitaliza tu Oficio Paso a Paso",
                "excerpt": "Guía práctica para carpinteros, herreros y reformistas que quieren dar el salto digital sin perder la esencia artesana.",
                "content": """
                    <h2>El Miedo a la Tecnología</h2>
                    <p>Muchos profesionales tradicionales temen que digitalizarse signifique perder el trato personal. Nada más lejos de la realidad. La tecnología debe servir para potenciar ese trato, automatizando lo aburrido (facturas, citas) para que tengas más tiempo para hablar con tus clientes y ejecutar tu trabajo con excelencia.</p>
                    
                    <h2>Herramientas Básicas para Empezar</h2>
                    <p>No necesitas un software de la NASA. Empieza por lo básico: una página web clara, un CRM sencillo para gestionar clientes y WhatsApp Business para comunicaciones rápidas. Estas tres herramientas, bien integradas, pueden liberarte de horas de gestión administrativa a la semana.</p>
                    
                    <h2>El Valor del Portafolio Digital</h2>
                    <p>Tu trabajo entra por los ojos. Una web te permite mostrar galerías de antes y después en alta resolución que un cliente no puede apreciar en una pantallita de móvil enviada por chat. Documentar tus procesos y mostrarlos al mundo es la mejor forma de justificar un precio premium por tu mano de obra.</p>
                """
            },
            {
                "slug": "importancia-resenas-online-reputacion",
                "title": "El Poder de las 5 Estrellas: Gestión de Reputación Online",
                "excerpt": "Las opiniones de desconocidos ahora valen tanto como la recomendación de un amigo. Aprende a gestionar y potenciar tus reseñas.",
                "content": """
                    <h2>La Nueva Moneda de Cambio</h2>
                    <p>El 93% de los consumidores leen reseñas online antes de contratar un servicio local. Una diferencia de 0.5 estrellas puede significar perder o ganar miles de euros al año. Las reseñas no son solo ego; son prueba social pura que valida tu promesa de valor.</p>
                    
                    <h2>Cómo Conseguir Más Reseñas</h2>
                    <p>El secreto es simple: pedirlo. Pero hay que saber cuándo y cómo. Una web profesional puede automatizar este proceso, enviando un recordatorio amable al cliente justo después de terminar un trabajo exitoso, facilitando el enlace directo a tu perfil de Google con un solo clic.</p>
                    
                    <h2>Responder es Obligatorio</h2>
                    <p>Responder a las reseñas, tanto positivas como negativas, demuestra que hay un humano detrás del negocio que se preocupa. Una respuesta bien redactada a una crítica negativa puede incluso convertir a un cliente enfadado en un defensor leal, y muestra a futuros clientes tu talante profesional ante los problemas.</p>
                """
            },
            {
                "slug": "futuro-servicios-locales-ia",
                "title": "El Futuro de los Servicios Locales: IA y Automatización",
                "excerpt": "No es ciencia ficción. Descubre cómo la Inteligencia Artificial ya está ayudando a fontaneros y pintores a ganar más dinero.",
                "content": """
                    <h2>Atención al Cliente 24/7 con Chatbots</h2>
                    <p>¿Pierdes trabajos porque estás subido a una escalera y no puedes coger el teléfono? Los chatbots inteligentes integrados en tu web pueden atender a esos clientes, cualificarlos y agendar una cita en tu calendario sin que tú tengas que dejar la herramienta. Esto no es el futuro, es el estándar que el cliente empieza a exigir.</p>
                    
                    <h2>Presupuestos Inteligentes</h2>
                    <p>Herramientas de IA pueden ayudar a generar presupuestos aproximados basados en fotos que envía el cliente, ahorrándote visitas improductivas. La tecnología está aquí para filtrar a los curiosos de los clientes reales, optimizando tu ruta de trabajo diaria.</p>
                    
                    <h2>LocalPro: Tu Socio Tecnológico</h2>
                    <p>En LocalPro, integramos estas tecnologías de vanguardia en webs accesibles para el pequeño profesional. Creemos que la IA no va a sustituir a los oficios, pero los profesionales que usen IA sustituirán a los que no la usen.</p>
                """
            }
        ]

    def _generate_post_html(self, article):
        # Very basic template for now, or read from file
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} - LocalPro Blog</title>
    <meta name="description" content="{article['excerpt']}">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../css/style.css"> <!-- Adjust path if needed -->
    <style>
        :root {{
            --primary: #3b82f6; 
            --secondary: #1e293b;
            --accent: #10b981;
            --background: #0f172a;
            --surface: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }}
        body {{
            background-color: var(--background);
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            line-height: 1.6;
        }}
        .blog-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .blog-header {{
            text-align: center;
            margin-bottom: 60px;
            padding-bottom: 40px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        h1 {{
            font-size: clamp(2rem, 4vw, 3rem);
            margin-bottom: 20px;
            color: var(--primary);
            line-height: 1.2;
        }}
        .meta {{
            color: var(--text-muted);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .blog-content {{
            font-size: 1.1rem;
            color: #cbd5e1;
        }}
        .blog-content h2 {{
            color: var(--text-main);
            margin-top: 40px;
            margin-bottom: 20px;
            font-size: 1.8rem;
        }}
        .blog-content p {{
            margin-bottom: 20px;
        }}
        .back-link {{
            display: inline-block;
            margin-top: 60px;
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
        }}
        .back-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="blog-container">
        <header class="blog-header">
            <div class="meta">Actualidad Digital • {datetime.now().year}</div>
            <h1>{article['title']}</h1>
            <p style="font-size: 1.2rem; max-width: 600px; margin: 0 auto; color: var(--text-muted);">{article['excerpt']}</p>
        </header>
        
        <article class="blog-content">
            {article['content']}
        </article>
        
        <a href="../../index.html" class="back-link">← Volver al inicio</a>
    </div>
</body>
</html>
        """

    def generate(self):
        full_output_dir = os.path.join(os.getcwd(), self.output_dir)
        os.makedirs(full_output_dir, exist_ok=True)
        
        generated_links = []
        
        for art in self.articles:
            html = self._generate_post_html(art)
            filename = f"{art['slug']}.html"
            filepath = os.path.join(full_output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            generated_links.append({
                "title": art['title'],
                "excerpt": art['excerpt'],
                "url": f"sites/blog/{filename}" # Relative to root for the hub? No, hub is in root.
                # Actually, hub is generated at sites/index.html. So links should be "blog/slug.html"
            })
            print(f"Generated blog post: {filepath}")

if __name__ == "__main__":
    gen = HubBlogGenerator()
    gen.generate()
