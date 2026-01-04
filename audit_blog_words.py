import os
import re

def count_words(html):
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', html)
    # Count words
    words = re.findall(r'\w+', text)
    return len(words)

from src.generator.blog_generator import BlogGenerator

gen = BlogGenerator()
for niche, articles in gen.niche_articles.items():
    print(f"--- {niche.upper()} ---")
    for i, art in enumerate(articles):
        word_count = count_words(art['content'])
        print(f"Article {i+1}: {word_count} words")
