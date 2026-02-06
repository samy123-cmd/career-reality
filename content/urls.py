from django.urls import path
from . import views

urlpatterns = [
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/og-image.svg', views.article_og_image, name='article_og_image'),
]
