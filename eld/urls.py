from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DriverViewSet, EldLogViewSet

router = DefaultRouter()
router.register(r'logs', EldLogViewSet, basename='log')
router.register(r'profile', DriverViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
