
import os

def fix_template(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Fix the primary color block
    import re
    # Match the broken pattern { { PRIMARY_COLOR } } or similar
    pattern = r'\{\s*\{\s*([A-Z_]+)\s*\}\s*\}'
    fixed = re.sub(pattern, r'[[\1]]', content)
    
    # Also handle the cases where it's split across multiple lines
    pattern_multiline = r'\{\s*\n\s*\{\s*\n\s*([A-Z_]+)\s*\n\s*\}\s*\n\s*\}'
    fixed = re.sub(pattern_multiline, r'[[\1]]', fixed)
    
    # One more broad one for the specific mess I see
    messy_pattern = r'\{\s+\{\s+([A-Z_]+)\s+\}\s+\}'
    fixed = re.sub(messy_pattern, r'[[\1]]', fixed)

    with open(path, 'w') as f:
        f.write(fixed)

fix_template('templates/site/index.html')
fix_template('templates/site/blog_post.html')
print("Templates fixed with [[BRACKETS]]")
