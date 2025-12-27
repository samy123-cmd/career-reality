from django.contrib import admin
from .models import AssessmentLog

@admin.register(AssessmentLog)
class AssessmentLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'risk_level', 'scenario_type', 'has_offer', 'tool_version')
    list_filter = ('risk_level', 'has_offer', 'tool_version', 'created_at')
    search_fields = ('scenario_type',)
    readonly_fields = ('created_at', 'risk_level', 'scenario_type', 'has_offer', 'tool_version')
    
    def has_add_permission(self, request):
        return False  # Logs are read-only
