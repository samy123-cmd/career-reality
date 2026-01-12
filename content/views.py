from django.shortcuts import render, get_object_or_404
from .models import Article, Category, Author

def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id, is_active=True)
    articles = Article.objects.filter(author=author, status='published').order_by('-published_at')
    return render(request, 'content/author_detail.html', {
        'author': author,
        'articles': articles
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
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
        'categories': categories
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # Filter only published articles, order by most recent
    articles = Article.objects.filter(category=category, status='published').order_by('-published_at')
    
    return render(request, 'content/category_detail.html', {
        'category': category,
        'articles': articles
    })
