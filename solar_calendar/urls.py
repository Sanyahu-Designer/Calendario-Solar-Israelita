from django.urls import path
from .views import get_solar_info

urlpatterns = [
    path('solar-info/', get_solar_info, name='solar_info'),
]
