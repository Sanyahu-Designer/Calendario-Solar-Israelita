from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, CalendarView, DateConverterView, SolarTimesView

router = DefaultRouter()
router.register(r'events', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('convert/', DateConverterView.as_view(), name='convert'),
    path('solar-times/', SolarTimesView.as_view(), name='solar-times'),
]
