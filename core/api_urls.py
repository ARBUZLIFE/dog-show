from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register('clubs', api_views.ClubViewSet, basename='api-club')
router.register('breeds', api_views.BreedViewSet, basename='api-breed')
router.register('owners', api_views.OwnerViewSet, basename='api-owner')
router.register('rings', api_views.RingViewSet, basename='api-ring')
router.register('experts', api_views.ExpertViewSet, basename='api-expert')
router.register('dogs', api_views.DogViewSet, basename='api-dog')
router.register('medals', api_views.MedalViewSet, basename='api-medal')
router.register('schedules', api_views.RingBreedScheduleViewSet, basename='api-schedule')

urlpatterns = [
    path('', include(router.urls)),
]