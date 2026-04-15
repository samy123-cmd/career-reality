from django.urls import path
from . import views

urlpatterns = [
    path("", views.company_directory, name="company_directory"),
    path("search/", views.company_search_api, name="company_search_api"),
    path("write-review/", views.write_review, name="write_review"),

    # Discussion hub (no company context)
    path("discussions/", views.discussion_list, name="discussion_list"),
    path("discussions/new/", views.discussion_create, name="discussion_create"),
    path("discussions/<int:pk>/", views.discussion_detail, name="discussion_detail"),
    path("discussions/<int:pk>/reply/", views.discussion_reply, name="discussion_reply"),
    path("discussions/<int:pk>/upvote/", views.discussion_upvote, name="discussion_upvote"),

    # Company-specific pages
    path("<slug:slug>/", views.company_detail, name="company_detail"),
    path("<slug:slug>/review/", views.submit_review, name="submit_review"),
    path("<slug:slug>/discuss/", views.discussion_create, name="company_discussion_create"),
]
