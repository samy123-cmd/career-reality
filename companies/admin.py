from django.contrib import admin
from .models import Company, CompanyReview, Discussion, DiscussionReply


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "sector", "size", "salary_count", "review_count", "overall_score", "is_verified"]
    list_filter = ["sector", "size", "is_verified", "work_mode"]
    search_fields = ["name", "headquarters"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["salary_count", "review_count", "layoff_report_count", "avg_ctc", "overall_score"]


@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ["company", "role_title", "rating_overall", "would_rejoin", "is_flagged", "created_at"]
    list_filter = ["is_flagged", "is_verified", "rating_overall", "employment_status"]
    search_fields = ["company__name", "role_title", "pros", "cons"]
    actions = ["flag_reviews", "unflag_reviews"]

    @admin.action(description="Flag selected reviews")
    def flag_reviews(self, request, queryset):
        queryset.update(is_flagged=True)

    @admin.action(description="Unflag selected reviews")
    def unflag_reviews(self, request, queryset):
        queryset.update(is_flagged=False)


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ["title", "topic", "company", "anonymous_handle", "upvotes", "is_flagged", "created_at"]
    list_filter = ["topic", "is_flagged", "is_pinned"]
    search_fields = ["title", "body", "anonymous_handle", "company__name"]
    raw_id_fields = ["company", "user"]
    actions = ["flag_selected", "unflag_selected", "pin_selected"]

    @admin.action(description="Flag selected discussions")
    def flag_selected(self, request, queryset):
        queryset.update(is_flagged=True)

    @admin.action(description="Unflag selected discussions")
    def unflag_selected(self, request, queryset):
        queryset.update(is_flagged=False)

    @admin.action(description="Pin selected discussions")
    def pin_selected(self, request, queryset):
        queryset.update(is_pinned=True)


@admin.register(DiscussionReply)
class DiscussionReplyAdmin(admin.ModelAdmin):
    list_display = ["discussion", "anonymous_handle", "is_flagged", "created_at"]
    list_filter = ["is_flagged"]
    search_fields = ["body", "anonymous_handle", "discussion__title"]
    raw_id_fields = ["discussion", "user"]
