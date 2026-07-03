from django.contrib import admin
from .models import UserProfile, CompanyWatchlist, LayoffAlertLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "tier", "is_pro", "subscription_expires_at", "salary_credits", "assessments_count", "created_at")
    list_filter = ("tier",)
    search_fields = ("user__email", "user__username")
    readonly_fields = ("created_at", "updated_at")


@admin.register(CompanyWatchlist)
class CompanyWatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "created_at")
    search_fields = ("user__email", "company__name")
    raw_id_fields = ("user", "company")


@admin.register(LayoffAlertLog)
class LayoffAlertLogAdmin(admin.ModelAdmin):
    list_display = ("user", "layoff_report", "sent_at")
    search_fields = ("user__email",)
    raw_id_fields = ("user", "layoff_report")
