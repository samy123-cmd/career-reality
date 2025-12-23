from django.shortcuts import render, get_object_or_404
from .models import Article, Category

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    return render(request, 'content/article_detail.html', {'article': article})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # Filter only published articles, order by most recent
    articles = Article.objects.filter(category=category, status='published').order_by('-published_at')
    
    return render(request, 'content/category_detail.html', {
        'category': category,
        'articles': articles
    })
