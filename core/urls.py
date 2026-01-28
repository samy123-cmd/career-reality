from django.urls import path
from . import views
from analyzer import views as analyzer_views

urlpatterns = [
    path('', views.home, name='home'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('about/', views.about, name='about'),
    path('editorial/', views.editorial_standards, name='editorial'),
    path('salary-reality/', views.salary_reality, name='salary_reality'),
    path('salary-calculator/', views.salary_calculator, name='salary_calculator'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    path('escape-plan/', views.escape_plan, name='escape_plan'),
    
    # Analyzer / Tools
    path('salary-drop/', analyzer_views.submit_salary, name='submit_salary'),
    path('salary-drop/success/', analyzer_views.salary_submit_success, name='salary_submit_success'),
    path('api/salary-feed/', analyzer_views.salary_feed_api, name='salary_feed_api'),
    
    # Layoff Radar
    path('layoff-radar/', analyzer_views.layoff_radar, name='layoff_radar'),
    path('layoff-radar/report/', analyzer_views.report_layoff, name='report_layoff'),
]

