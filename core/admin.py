from django.contrib import admin
from .models import NewsletterSubscriber, CareerRealityIndexSnapshot


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)


@admin.register(CareerRealityIndexSnapshot)
class CareerRealityIndexSnapshotAdmin(admin.ModelAdmin):
    list_display = ['month', 'salary_pressure', 'switch_difficulty', 'layoff_risk', 'overall',
                    'total_salary_submissions', 'total_layoff_reports', 'computed_at']
    readonly_fields = ['computed_at']
    ordering = ['-month_date']
