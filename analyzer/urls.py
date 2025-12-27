from django.urls import path
from . import views

urlpatterns = [
    # SEO Landing Page
    path('', views.intro_view, name='analyzer_home'),
    
    # Start Action (POST)
    path('start/', views.wizard_start_session, name='wizard_start'),
    
    # Step handling
    path('step/<int:step>/', views.wizard_step, name='wizard_step'),
    
    # Result page
    path('result/', views.result_view, name='wizard_result'),
]
