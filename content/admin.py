from django.contrib import admin
from .models import Article, Category, Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'is_active')
    search_fields = ('name', 'display_name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_hi', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'published_at', 'last_reality_check')
    list_filter = ('status', 'category', 'author', 'last_reality_check')
    search_fields = ('title', 'target_persona', 'verdict')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Publishing', {
            'fields': ('title', 'title_hi', 'slug', 'author', 'category', 'status', 'published_at', 'updated_at', 'last_reality_check')
        }),
        ('SEO Metadata', {
            'fields': (
                ('meta_title', 'meta_title_hi'),
                ('meta_description', 'meta_description_hi')
            )
        }),
        ('Strict Reality Content (English)', {
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
        ('Strict Reality Content (Hindi)', {
            'fields': (
                'target_persona_hi', 
                'who_should_avoid_hi',
                'common_expectation_hi', 
                'actual_reality_hi', 
                'salary_reality_hi', 
                'stuck_point_hi', 
                'verdict_hi'
            ),
            'description': "Hindi translations of the reality content.",
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('updated_at',)
