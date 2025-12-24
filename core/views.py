from django.shortcuts import render
from content.models import Article, Category

def home(request):
    """
    Home page view.
    - Shows mission statement.
    - Lists only PUBLISHED articles.
    """
    articles = Article.objects.filter(status='published').select_related('author', 'category').order_by('-published_at')
    categories = Category.objects.all()
    
    return render(request, 'core/home.html', {
        'articles': articles,
        'categories': categories,
    })

def about(request):
    return render(request, 'core/about.html')

def editorial_standards(request):
    return render(request, 'core/editorial.html')

def salary_reality(request):
    return render(request, 'core/salary.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')
