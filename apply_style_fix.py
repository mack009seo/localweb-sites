import os
import re

def apply_css_fix():
    sites_dir = "sites"
    
    css_to_add = """
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
    count = 0
    for root, dirs, files in os.walk(sites_dir):
        if "style.css" in files:
            path = os.path.join(root, "style.css")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # If accidentally added before or incomplete, we replace/update it
            if ".btn-demo" in content:
                # Remove existing .btn-demo and .btn-demo:hover blocks
                new_content = re.sub(r'\.btn-demo\s*\{[^}]*\}', '', content)
                new_content = re.sub(r'\.btn-demo:hover\s*\{[^}]*\}', '', new_content)
                new_content = new_content.strip() + "\n" + css_to_add
            else:
                new_content = content.strip() + "\n" + css_to_add
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                count += 1
                
    print(f"✓ Estilos actualizados en {count} archivos style.css")

def update_blog_pages():
    sites_dir = "sites"
    count = 0
    # New style for back-link from template
    new_style = """
        .back-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 20px;
            color: var(--accent);
            text-decoration: none;
            font-weight: 700;
            background: rgba(255,255,255,0.05);
            padding: 8px 15px;
            border-radius: 8px;
            transition: var(--transition);
        }

        .back-link:hover {
            background: rgba(255,255,255,0.1);
            transform: translateX(-5px);
        }

        .article-body a {
            color: var(--accent);
            text-decoration: underline;
            font-weight: 600;
        }
    """
    
    for root, dirs, files in os.walk(sites_dir):
        for file in files:
            if file.endswith(".html") and "blog" in root:
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Update root vars formatting if messy
                content = re.sub(r'--primary:\s*hsl\([^)]+\)\s*;', lambda m: m.group(0).strip(), content)
                
                # Update .back-link style
                if ".back-link {" in content:
                    new_content = re.sub(r'\.back-link\s*\{[^}]*\}', new_style, content)
                    if new_content != content:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        count += 1
    print(f"✓ Páginas de blog actualizadas: {count}")

if __name__ == "__main__":
    apply_css_fix()
    update_blog_pages()
