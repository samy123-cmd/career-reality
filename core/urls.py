from django.urls import path
from . import views
from analyzer import views as analyzer_views

urlpatterns = [
    path('', views.home, name='home'),
    path('healthz', views.healthz, name='healthz'),
    path('internal/cron/freshness/', views.run_freshness_cron, name='run_freshness_cron'),
    path('internal/cron/weekly-digest/', views.run_weekly_digest_cron, name='run_weekly_digest_cron'),
    path('internal/cron/refresh-career-index/', views.run_career_index_cron, name='run_career_index_cron'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('about/', views.about, name='about'),
    path('editorial/', views.editorial_standards, name='editorial'),
    path('salary-reality/', views.salary_reality, name='salary_reality'),
    path('salary-calculator/', views.salary_calculator, name='salary_calculator'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('topic-clusters/', views.topic_clusters, name='topic_clusters'),
    path('career-reality-index/', views.career_reality_index, name='career_reality_index'),
    path('revenue-model/', views.revenue_model, name='revenue_model'),
    path('sponsorship-policy/', views.sponsorship_policy, name='sponsorship_policy'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    path('newsletter/unsubscribe/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('offline/', views.offline_view, name='offline'),
    path('escape-plan/', views.escape_plan, name='escape_plan'),
    path('pro/', views.pricing_redirect, name='pro_landing'),
    
    # Analyzer / Tools
    path('salary-drop/', analyzer_views.submit_salary, name='submit_salary'),
    path('salary-drop/success/', analyzer_views.salary_submit_success, name='salary_submit_success'),
    path('api/salary-feed/', analyzer_views.salary_feed_api, name='salary_feed_api'),
    path('api/events/', analyzer_views.track_event_api, name='track_event_api'),
    
    # Layoff Radar
    path('layoff-radar/', analyzer_views.layoff_radar, name='layoff_radar'),
    path('layoff-radar/report/', analyzer_views.report_layoff, name='report_layoff'),
]

