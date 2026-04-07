from django.urls import path
from . import views

urlpatterns = [
    path("", views.company_directory, name="company_directory"),
    path("search/", views.company_search_api, name="company_search_api"),
    path("<slug:slug>/", views.company_detail, name="company_detail"),
    path("<slug:slug>/review/", views.submit_review, name="submit_review"),
]
