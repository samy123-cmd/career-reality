from django.urls import path
from . import views

urlpatterns = [
    path("onboarding/", views.onboarding, name="onboarding"),
    path("dashboard/", views.pro_dashboard, name="pro_dashboard"),
    path("my-career-reality/", views.my_career_reality, name="my_career_reality"),
    path("career-profile/", views.career_profile_edit, name="career_profile_edit"),
    path("progression/", views.career_progression, name="career_progression"),
    path("risk-radar/", views.career_risk_radar, name="career_risk_radar"),
    path("risk-radar/alerts/<int:alert_id>/read/", views.mark_alert_read, name="mark_alert_read"),
    path("watchlist/<slug:slug>/toggle/", views.toggle_watchlist, name="toggle_watchlist"),
]
