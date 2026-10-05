from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/participants/', views.catalog_participants, name='catalog_participants'),
    path('catalog/exhibitions/', views.catalog_exhibitions, name='catalog_exhibitions'),

    # Собаки
    path('dogs/', views.DogListView.as_view(), name='dog_list'),
    path('dogs/create/', views.DogCreateView.as_view(), name='dog_create'),
    path('dogs/<int:pk>/update/', views.DogUpdateView.as_view(), name='dog_update'),
    path('dogs/<int:pk>/delete/', views.DogDeleteView.as_view(), name='dog_delete'),

    # Клубы
    path('clubs/', views.ClubListView.as_view(), name='club_list'),
    path('clubs/create/', views.ClubCreateView.as_view(), name='club_create'),
    path('clubs/<int:pk>/update/', views.ClubUpdateView.as_view(), name='club_update'),
    path('clubs/<int:pk>/delete/', views.ClubDeleteView.as_view(), name='club_delete'),

    # Породы
    path('breeds/', views.BreedListView.as_view(), name='breed_list'),
    path('breeds/create/', views.BreedCreateView.as_view(), name='breed_create'),
    path('breeds/<int:pk>/update/', views.BreedUpdateView.as_view(), name='breed_update'),
    path('breeds/<int:pk>/delete/', views.BreedDeleteView.as_view(), name='breed_delete'),

    # Хозяева
    path('owners/', views.OwnerListView.as_view(), name='owner_list'),
    path('owners/create/', views.OwnerCreateView.as_view(), name='owner_create'),
    path('owners/<int:pk>/update/', views.OwnerUpdateView.as_view(), name='owner_update'),
    path('owners/<int:pk>/delete/', views.OwnerDeleteView.as_view(), name='owner_delete'),

    # Ринги
    path('rings/', views.RingListView.as_view(), name='ring_list'),
    path('rings/create/', views.RingCreateView.as_view(), name='ring_create'),
    path('rings/<int:pk>/update/', views.RingUpdateView.as_view(), name='ring_update'),
    path('rings/<int:pk>/delete/', views.RingDeleteView.as_view(), name='ring_delete'),

    # Эксперты
    path('experts/', views.ExpertListView.as_view(), name='expert_list'),
    path('experts/create/', views.ExpertCreateView.as_view(), name='expert_create'),
    path('experts/<int:pk>/update/', views.ExpertUpdateView.as_view(), name='expert_update'),
    path('experts/<int:pk>/delete/', views.ExpertDeleteView.as_view(), name='expert_delete'),

    # Медали
    path('medals/', views.MedalListView.as_view(), name='medal_list'),
    path('medals/create/', views.MedalCreateView.as_view(), name='medal_create'),
    path('medals/<int:pk>/update/', views.MedalUpdateView.as_view(), name='medal_update'),
    path('medals/<int:pk>/delete/', views.MedalDeleteView.as_view(), name='medal_delete'),

    # Расписания
    path('schedules/', views.ScheduleListView.as_view(), name='schedule_list'),
    path('schedules/create/', views.ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedules/<int:pk>/update/', views.ScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedules/<int:pk>/delete/', views.ScheduleDeleteView.as_view(), name='schedule_delete'),
]