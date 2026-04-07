from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "tier", "is_pro", "subscription_expires_at", "assessments_count", "created_at")
    list_filter = ("tier",)
    search_fields = ("user__email", "user__username")
    readonly_fields = ("created_at", "updated_at")
