"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.sitemap_view import cached_sitemap
from core import views as core_views

handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'

from django.conf.urls.i18n import i18n_patterns

# Non-translated URLs (payment endpoints must not be under i18n prefix for webhooks)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('sitemap.xml', cached_sitemap, name='cached_sitemap'),
    path('payments/', include('payments.urls', namespace='payments')),
    path('accounts/', include('allauth.urls')),
    # Required by Google AdSense — must be at root domain, not under any prefix
    path('ads.txt', core_views.ads_txt, name='ads_txt'),
    # Ops / deploy verification — outside i18n so /healthz/ always resolves
    path('healthz/', core_views.healthz, name='healthz'),
]

# Translated URLs
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('', include('content.urls')),
    path('ai/', include('ainews.urls')),
    path('resignation-risk/', include('analyzer.urls')),
    path('pro/', include('accounts.urls')),
    path('companies/', include('companies.urls')),
    path('search/', include('search.urls')),
    prefix_default_language=False  # Only prefix non-default languages (e.g., /hi/)
)
