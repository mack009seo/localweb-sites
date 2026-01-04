---
description: How to configure a custom domain for GitHub Pages
---

# Configuración de Dominio Personalizado en GitHub Pages

Para que tu directorio y las webs de tus clientes se vean profesionales (ej: `tudominio.com/negocio`), sigue estos pasos:

## 1. Configuración en el registrador de dominios (ej: Namecheap, GoDaddy)

Debes añadir los siguientes registros DNS en el panel de tu dominio:

### A Records (Puntan a GitHub)
Añade 4 registros tipo **A** que apunten a estas IPs de GitHub:
- `185.199.108.153`
- `185.199.109.153`
- `185.199.110.153`
- `185.199.111.153`

### CNAME Record (Para el subdominio www)
- Tipo: `CNAME`
- Host: `www`
- Valor: `mack009seo.github.io`

---

## 2. Configuración en GitHub

1. Entra en tu repositorio `localweb-sites`.
2. Ve a **Settings > Pages**.
3. En la sección **Custom domain**, escribe tu dominio (ej: `serviciosbarcelona.com`).
4. Dale a **Save**.
5. Marca la casilla **Enforce HTTPS** (puede tardar unos minutos en estar disponible mientras se genera el certificado SSL).

> [!TIP]
> También puedes crear un archivo llamado `CNAME` (sin extensión) en la raíz de tu carpeta `sites/` con el nombre de tu dominio dentro.

---

## 3. Estructura de las URLs finales

Una vez configurado, las URLs pasarán de ser largas a cortas y profesionales:

| Elemento | URL Actual (GitHub) | URL con Dominio Propio |
| :--- | :--- | :--- |
| **Directorio** | `https://mack009seo.github.io/localweb-sites/` | `https://tudominio.com/` |
| **Negocio** | `https://mack009seo.github.io/localweb-sites/negocio-slug/` | `https://tudominio.com/negocio-slug/` |
| **Blog** | `https://mack009seo.github.io/localweb-sites/negocio-slug/blog/post.html` | `https://tudominio.com/negocio-slug/blog/post.html` |

---

## 4. ¿Qué debo cambiar en el código?

En `src/automate.py`, debes actualizar la variable `demo_url` para que los mensajes de WhatsApp lleven el nuevo dominio:

```python
# En src/automate.py (Línea ~41)
demo_url = f"https://tudominio.com/{slug}/"
```

> [!IMPORTANT]
> Al usar un dominio propio, Google indexará tu sitio mucho mejor y la confianza de los clientes al recibir el link por WhatsApp será mucho mayor.
