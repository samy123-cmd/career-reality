from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_news_hub, name='ai_news_hub'),
    path('tag/<slug:slug>/', views.ai_news_by_tag, name='ai_news_by_tag'),
    path('<slug:slug>/', views.ai_news_detail, name='ai_news_detail'),
]
