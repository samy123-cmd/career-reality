from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('editorial/', views.editorial_standards, name='editorial'),
    path('salary-reality/', views.salary_reality, name='salary_reality'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
