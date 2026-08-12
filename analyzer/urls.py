from django.urls import path
from . import views, views_tools

urlpatterns = [
    # Resignation Risk Analyzer
    path('', views.intro_view, name='analyzer_home'),
    path('start/', views.wizard_start_session, name='wizard_start'),
    path('step/<int:step>/', views.wizard_step, name='wizard_step'),
    path('result/', views.result_view, name='wizard_result'),
]

# Career tools mounted at /tools/ in core/urls.py
tools_urlpatterns = [
    path('salary-reality-engine/', views_tools.salary_reality_engine, name='salary_reality_engine'),
    path('offer-analyzer/', views_tools.offer_analyzer, name='offer_analyzer'),
    path('stay-vs-switch/', views_tools.stay_vs_switch, name='stay_vs_switch'),
    path('ai-career-impact/', views_tools.ai_career_impact, name='ai_career_impact'),
    path('next-career-move/', views_tools.next_career_move, name='next_career_move'),
    path('ask/', views_tools.ask_career_reality, name='ask_career_reality'),
]
