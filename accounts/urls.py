from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.pro_dashboard, name="pro_dashboard"),
]
