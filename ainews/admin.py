from django.contrib import admin
from .models import AITag, AINewsItem, AINewsFetchRun


@admin.register(AITag)
class AITagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(AINewsItem)
class AINewsItemAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'source_name', 'significance', 'status', 'fact_check_status',
        'event_date', 'reviewed_at', 'published_at'
    )
    list_filter = ('status', 'fact_check_status', 'significance', 'tags', 'source_name')
    search_fields = ('title', 'summary', 'career_angle')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'reviewed_at'
    filter_horizontal = ('tags',)

    fieldsets = (
        ('Publishing', {
            'fields': (
                'title', 'slug', 'status', 'fact_check_status', 'significance',
                'event_date', 'reviewed_at', 'published_at'
            )
        }),
        ('Content', {
            'fields': ('summary', 'career_angle', 'tags')
        }),
        ('Review Workflow', {
            'fields': ('reviewed_by', 'last_verified_at', 'review_notes')
        }),
        ('Source', {
            'fields': ('source_name', 'source_url', 'external_id')
        }),
    )


@admin.register(AINewsFetchRun)
class AINewsFetchRunAdmin(admin.ModelAdmin):
    list_display = (
        'started_at', 'finished_at', 'status',
        'total_created', 'total_skipped', 'total_warnings', 'total_errors', 'source_count'
    )
    list_filter = ('status',)
    readonly_fields = (
        'started_at', 'finished_at', 'status',
        'total_created', 'total_skipped', 'total_warnings', 'total_errors', 'source_count', 'notes'
    )
    search_fields = ('notes',)
