from datetime import date, timedelta
from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Category, Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'is_active')
    search_fields = ('name', 'display_name')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)


def mark_reality_checked_today(modeladmin, request, queryset):
    """Admin bulk action: set last_reality_check to today for selected articles."""
    today = date.today()
    updated = queryset.update(last_reality_check=today)
    modeladmin.message_user(
        request,
        f"{updated} article(s) marked as reality-checked on {today}."
    )

mark_reality_checked_today.short_description = "✅ Mark selected as reality-checked today"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'published_at', 'freshness_status')
    list_filter = ('status', 'category', 'author', 'last_reality_check')
    search_fields = ('title', 'target_persona', 'verdict')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    actions = [mark_reality_checked_today]

    def freshness_status(self, obj):
        if not obj.last_reality_check:
            return format_html('<span style="color:#ef4444;font-weight:bold;">⚠ NEVER CHECKED</span>')
        days = (date.today() - obj.last_reality_check).days
        if days <= 30:
            color, label = '#22c55e', f'✓ Fresh ({days}d ago)'
        elif days <= 60:
            color, label = '#f59e0b', f'~ Aging ({days}d ago)'
        else:
            color, label = '#ef4444', f'✗ Stale ({days}d ago)'
        return format_html('<span style="color:{};">{}</span>', color, label)

    freshness_status.short_description = 'Freshness'
    freshness_status.admin_order_field = 'last_reality_check'

    fieldsets = (
        ('Publishing', {
            'fields': ('title', 'slug', 'author', 'category', 'status', 'published_at', 'updated_at', 'last_reality_check')
        }),
        ('SEO Metadata', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Strict Reality Content', {
            'fields': (
                'target_persona',
                'who_should_avoid',
                'common_expectation',
                'actual_reality',
                'salary_reality',
                'stuck_point',
                'verdict'
            ),
            'description': "MUST be filled with honest, non-hype content."
        }),
    )
    readonly_fields = ('updated_at',)

