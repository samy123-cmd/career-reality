from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path("create-order/", views.create_order, name="create_order"),
    path("verify/", views.verify_payment, name="verify"),
    path("webhook/", views.razorpay_webhook, name="webhook"),
    path("pricing/", views.pricing, name="pricing"),
]
