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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/solar/', include('core.urls')),
    path('api/solar-times/', include('solar_calendar.urls')),  
    path('solar/', ViteAppView.as_view(), name='solar-calendar'),
    path('biodynamic/', ViteAppView.as_view(), name='biodynamic-calendar'),
    path('', RedirectView.as_view(url='/solar/', permanent=False), name='home'),
    path('<path:path>', ViteAppView.as_view(), name='vite-app-with-path'),
]
