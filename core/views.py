from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from content.models import Article, Category

def robots_txt(request):
    """
    Serves the robots.txt file dynamically.
    """
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def home(request):
    """
    Home page view.
    - Shows mission statement.
    - Lists only PUBLISHED articles.
    """
    articles = Article.objects.filter(status='published').select_related('author', 'category').order_by('-published_at')[:10]
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

def salary_calculator(request):
    """In-hand salary calculator for Indian professionals."""
    categories = Category.objects.all()
    return render(request, 'core/salary_calculator.html', {'categories': categories})

def escape_plan(request):
    """
    The Service Company Escape Plan.
    Contains the "Rot Check" quiz and the roadmap.
    """
    return render(request, 'content/escape_plan.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def contact(request):
    return render(request, 'core/contact.html')

def terms(request):
    return render(request, 'core/terms.html')

def newsletter_signup(request):
    """Handle newsletter signup form submission."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            # For now, just show a success message
            # In production, integrate with Mailchimp/Buttondown/database
            from core.models import NewsletterSubscriber
            try:
                NewsletterSubscriber.objects.get_or_create(email=email)
                messages.success(request, 'Thanks for subscribing! You\'ll get our weekly reality checks.')
            except Exception:
                messages.info(request, 'Thanks for your interest!')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    # Redirect back to the previous page
    return redirect(request.META.get('HTTP_REFERER', 'home'))

