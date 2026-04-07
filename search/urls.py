from django.urls import path
from . import views

urlpatterns = [
    path("", views.search_view, name="search"),
    path("suggest/", views.search_suggest_api, name="search_suggest"),
]
