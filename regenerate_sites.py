import os
import re
import shutil
from src.generator.blog_generator import BlogGenerator

def extract_colors_from_css(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    primary = re.search(r'--primary:\s*([^;]+);', content)
    primary_hover = re.search(r'--primary-hover:\s*([^;]+);', content)
    accent = re.search(r'--accent:\s*([^;]+);', content)
    
    return {
        "primary": primary.group(1) if primary else "#6366f1",
        "primary_hover": primary_hover.group(1) if primary_hover else "#4f46e5",
        "accent": accent.group(1) if accent else "#f59e0b"
    }

def extract_info_from_index(index_path):
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract phone from JSON-LD or meta or anywhere
    phone = re.search(r'"telephone":\s*"([^"]+)"', content)
    if not phone:
        phone = re.search(r'tel:([^"]+)', content)
    
    # Extract biz name
    biz_name = re.search(r'"name":\s*"([^"]+)"', content)
    if not biz_name:
        biz_name = re.search(r'<title>([^|]+)', content)
        
    return {
        "phone": phone.group(1) if phone else "600000000",
        "biz_name": biz_name.group(1).strip() if biz_name else "Tu Negocio"
    }

def fix_index_html(index_path):
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove inline padding from blog links
    new_content = re.sub(r'class="btn btn-demo" style="([^"]*?)padding:\s*8px;?\s*([^"]*?)"', r'class="btn btn-demo" style="\1\2"', content)
    
    # Fix blog section title
    new_content = new_content.replace('<h2>Consejos y Actualidades</h2>', '<h2>Consejos</h2>')
    
    if new_content != content:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def regenerate_all():
    sites_dir = "sites"
    template_css = "templates/site/assets/css/style.css"
    blog_gen = BlogGenerator()
    
    count_css = 0
    count_index = 0
    count_blog = 0
    
    for site_name in os.listdir(sites_dir):
        site_path = os.path.join(sites_dir, site_name)
        if not os.path.isdir(site_path):
            continue
            
        index_path = os.path.join(site_path, "index.html")
        css_path = os.path.join(site_path, "assets", "css", "style.css")
        
        if not os.path.exists(index_path) or not os.path.exists(css_path):
            continue
            
        # 1. Extract info
        colors = extract_colors_from_css(css_path)
        info = extract_info_from_index(index_path)
        
        # 2. Update CSS from template
        shutil.copy(template_css, css_path)
        
        # Re-apply dynamic colors to the new style.css
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            
        css_content = css_content.replace("--primary: #6366f1;", f"--primary: {colors['primary']};")
        css_content = css_content.replace("--primary-hover: #4f46e5;", f"--primary-hover: {colors['primary_hover']};")
        css_content = css_content.replace("--accent: #f59e0b;", f"--accent: {colors['accent']};")
        
        # Add the .btn-demo fix at the end (the high contrast version)
        btn_demo_fix = """
.btn-demo {
    background: var(--white);
    color: var(--primary);
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    text-align: center;
    border-radius: 10px;
    font-weight: 700;
}

.btn-demo:hover {
    background: var(--primary);
    color: var(--white);
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}
"""
        css_content = css_content.strip() + "\n" + btn_demo_fix
        
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css_content)
        count_css += 1
        
        # 3. Fix Index HTML
        if fix_index_html(index_path):
            count_index += 1
            
        # 4. Regenerate Blog
        # Guess category from site_name
        category = site_name.split("-")[0]
        blog_gen.generate_blog(
            site_path, 
            category, 
            info['biz_name'], 
            colors['primary'], 
            colors['primary_hover'], 
            colors['accent'], 
            info['phone'],
            site_name
        )
        count_blog += 1
        
    print(f"✓ CSS actualizado en {count_css} sitios")
    print(f"✓ index.html corregido en {count_index} sitios")
    print(f"✓ Blog regenerado en {count_blog} sitios")

if __name__ == "__main__":
    regenerate_all()
