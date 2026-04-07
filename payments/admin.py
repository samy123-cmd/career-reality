from django.contrib import admin
from .models import Product, Order, Subscription


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "price_paise", "product_type", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "status", "amount_paise", "email", "created_at")
    list_filter = ("status", "product")
    search_fields = ("email", "razorpay_order_id", "razorpay_payment_id")
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "tier", "status", "started_at", "expires_at")
    list_filter = ("tier", "status")
    search_fields = ("user__email",)
