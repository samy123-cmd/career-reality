from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.cache import cache_page
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

@cache_page(300)
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

def _seo(title, description):
    return {
        'og_title': title,
        'og_description': description,
        'twitter_title': title,
        'twitter_description': description,
    }

def about(request):
    title = "About Career Reality - India Career Truths"
    description = "Why Career Reality exists, who it serves, and how we cover Indian tech careers with independent, data-backed analysis."
    return render(request, 'core/about.html', _seo(title, description))

def editorial_standards(request):
    title = "Editorial Standards - Career Reality India"
    description = "Editorial principles for Career Reality: accuracy over comfort, no sponsored influence, and transparent updates to reflect market shifts."
    return render(request, 'core/editorial.html', _seo(title, description))

def salary_reality(request):
    title = "Salary Reality (India) - Career Reality"
    description = "Real, uninflated salary data for Indian tech roles with context and median ranges."
    return render(request, 'core/salary.html', _seo(title, description))

def salary_calculator(request):
    """In-hand salary calculator for Indian professionals."""
    categories = Category.objects.all()
    title = "CTC Decoder: Calculate In-Hand Salary India (2026)"
    description = "Decode CTC into real in-hand salary with PF, gratuity, variable pay, and tax regime logic."
    context = {'categories': categories}
    context.update(_seo(title, description))
    return render(request, 'core/salary_calculator.html', context)

def escape_plan(request):
    """
    The Service Company Escape Plan.
    Contains the "Rot Check" quiz and the roadmap.
    """
    return render(request, 'content/escape_plan.html')

def privacy_policy(request):
    title = "Privacy Policy - Career Reality India"
    description = "Privacy Policy for Career Reality India. Covers cookies, data collection, and ad network compliance."
    return render(request, 'core/privacy_policy.html', _seo(title, description))

def contact(request):
    title = "Contact Career Reality - Editorial Inquiries"
    description = "Contact Career Reality for editorial inquiries, corrections, or feedback on our India career analysis."
    return render(request, 'core/contact.html', _seo(title, description))

def terms(request):
    title = "Terms of Service - Career Reality India"
    description = "Terms of Service for Career Reality India. Read before using the site and its career content."
    return render(request, 'core/terms.html', _seo(title, description))

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

