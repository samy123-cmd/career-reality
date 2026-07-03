from django.contrib import admin
from .models import AssessmentLog, FunnelEventLog, SalarySubmission, LayoffReport


@admin.action(description="Mark selected as verified")
def mark_verified(modeladmin, request, queryset):
    queryset.update(verification_status="verified", is_verified=True)


@admin.register(SalarySubmission)
class SalarySubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'role', 'company_name', 'company', 'company_type', 'ctc', 'city',
        'experience_years', 'verification_status', 'is_verified', 'source', 'created_at',
    ]
    list_filter = ['company_type', 'verification_status', 'is_verified', 'city', 'source']
    search_fields = ['role', 'company_name', 'city', 'tech_stack']
    raw_id_fields = ['company']
    actions = [mark_verified]


@admin.register(LayoffReport)
class LayoffReportAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company', 'status', 'role_affected', 'location', 'is_verified', 'created_at']
    list_filter = ['status', 'is_verified']
    search_fields = ['company_name', 'role_affected', 'location']
    raw_id_fields = ['company']


@admin.register(AssessmentLog)
class AssessmentLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'risk_level', 'scenario_type', 'has_offer', 'tool_version')
    list_filter = ('risk_level', 'has_offer', 'tool_version', 'created_at')
    search_fields = ('scenario_type',)
    readonly_fields = ('created_at', 'risk_level', 'scenario_type', 'has_offer', 'tool_version')
    
    def has_add_permission(self, request):
        return False  # Logs are read-only


@admin.register(FunnelEventLog)
class FunnelEventLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'event_name', 'session_id', 'page_path')
    list_filter = ('event_name', 'created_at')
    search_fields = ('session_id', 'page_path', 'metadata')
    readonly_fields = ('created_at', 'event_name', 'session_id', 'page_path', 'user_agent', 'metadata')

    def has_add_permission(self, request):
        return False
