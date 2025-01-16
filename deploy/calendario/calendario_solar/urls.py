"""
URL configuration for calendario_solar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .views import ViteAppView
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/solar/', include('core.urls')),
    path('api/solar-times/', include('core.urls')),  # Mantendo a rota antiga para compatibilidade
    
    # Frontend Routes
    path('solar/', ViteAppView.as_view(), name='solar-calendar'),
    path('solar/<path:path>', ViteAppView.as_view(), name='solar-calendar-path'),
    path('', RedirectView.as_view(url='/solar/', permanent=False), name='home'),
]

# Add static files handling if in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
