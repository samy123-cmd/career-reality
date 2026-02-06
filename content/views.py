from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import escape
from django.views.decorators.cache import cache_page
from .models import Article, Category, Author

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id, is_active=True)
    articles = Article.objects.filter(author=author, status='published').order_by('-published_at')
    return render(request, 'content/author_detail.html', {
        'author': author,
        'articles': articles
    })

@cache_page(300)
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    og_image_url = request.build_absolute_uri(reverse('article_og_image', args=[article.slug]))
    # Get related articles from the same category, excluding the current article
    related_articles = Article.objects.filter(
        category=article.category,
        status='published'
    ).exclude(id=article.id).order_by('-published_at')[:3]
    # Get all categories for internal linking
    categories = Category.objects.all()
    return render(request, 'content/article_detail.html', {
        'article': article,
        'related_articles': related_articles,
        'categories': categories,
        'article_meta_title': article.meta_title,
        'article_meta_description': article.meta_description,
        'og_type': 'article',
        'og_title': article.meta_title,
        'og_description': article.meta_description,
        'og_image': og_image_url,
        'twitter_title': article.meta_title,
        'twitter_description': article.meta_description,
        'twitter_image': og_image_url,
    })

@cache_page(300)
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    og_title = f"{category.name} Careers in India - Career Reality"
    og_description = f"Reality checks and insights about {category.name.lower()} careers in India. Salary expectations, trade-offs, and growth risks."
    # Filter only published articles, order by most recent
    articles = Article.objects.filter(category=category, status='published').order_by('-published_at')
    
    return render(request, 'content/category_detail.html', {
        'category': category,
        'articles': articles,
        'og_title': og_title,
        'og_description': og_description,
        'twitter_title': og_title,
        'twitter_description': og_description,
    })

def article_og_image(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')

    def wrap_text(text, max_chars=34, max_lines=3):
        words = text.split()
        lines = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
            if len(lines) == max_lines:
                break
        if len(lines) < max_lines and current:
            lines.append(current)
        if len(lines) > max_lines:
            lines = lines[:max_lines]
        if len(lines) == max_lines and words and " ".join(lines) != text:
            lines[-1] = (lines[-1][: max_chars - 3] + "...") if len(lines[-1]) > 3 else "..."
        return lines

    title_lines = wrap_text(article.title)
    category = escape(article.category.name)

    y_start = 210
    line_height = 64
    title_svg = "\n".join(
        f'<text x="140" y="{y_start + i * line_height}" fill="#ffffff" '
        f'font-family="Inter, Segoe UI, Arial, sans-serif" font-size="54" '
        f'font-weight="700" letter-spacing="-0.5">{escape(line)}</text>'
        for i, line in enumerate(title_lines)
    )

    svg = f"""<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Career Reality article preview">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d0d0d"/>
      <stop offset="100%" stop-color="#1c1c1c"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#d93025"/>
      <stop offset="100%" stop-color="#ff6f61"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect x="88" y="88" width="10" height="454" fill="url(#accent)"/>
  {title_svg}
  <text x="140" y="470" fill="#d8d8d8" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="30" font-weight="500">
    {category}
  </text>
  <rect x="140" y="505" width="430" height="56" rx="8" fill="#111111" stroke="#3a3a3a"/>
  <text x="164" y="542" fill="#ffffff" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="24" font-weight="600">
    careerreality.in
  </text>
</svg>"""

    response = HttpResponse(svg, content_type="image/svg+xml")
    response["Cache-Control"] = "public, max-age=86400"
    return response
