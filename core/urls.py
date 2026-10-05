from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('dogs/', views.dog_list, name='dog_list'),
    path('dogs/create/', views.dog_create, name='dog_create'),
    path('dogs/<int:pk>/update/', views.dog_update, name='dog_update'),
    path('dogs/<int:pk>/delete/', views.dog_delete, name='dog_delete'),
]