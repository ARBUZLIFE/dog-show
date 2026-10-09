from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Каталоги
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/participants/', views.catalog_participants, name='catalog_participants'),
    path('catalog/exhibitions/', views.catalog_exhibitions, name='catalog_exhibitions'),
    path('catalog/medals/', views.catalog_medals, name='catalog_medals'),

    # Собаки
    path('dogs/', views.DogListView.as_view(), name='dog_list'),
    path('dogs/create/', views.DogCreateView.as_view(), name='dog_create'),
    path('dogs/<int:pk>/', views.DogDetailView.as_view(), name='dog_detail'),
    path('dogs/<int:pk>/update/', views.DogUpdateView.as_view(), name='dog_update'),
    path('dogs/<int:pk>/delete/', views.DogDeleteView.as_view(), name='dog_delete'),
    path('dogs/<int:pk>/disqualify/', views.DogDisqualifyView.as_view(), name='dog_disqualify'),
    path('dogs/<int:pk>/restore/', views.DogRestoreView.as_view(), name='dog_restore'),

    # Клубы
    path('clubs/', views.ClubListView.as_view(), name='club_list'),
    path('clubs/create/', views.ClubCreateView.as_view(), name='club_create'),
    path('clubs/<int:pk>/', views.ClubDetailView.as_view(), name='club_detail'),
    path('clubs/<int:pk>/update/', views.ClubUpdateView.as_view(), name='club_update'),
    path('clubs/<int:pk>/delete/', views.ClubDeleteView.as_view(), name='club_delete'),

    # Породы
    path('breeds/', views.BreedListView.as_view(), name='breed_list'),
    path('breeds/create/', views.BreedCreateView.as_view(), name='breed_create'),
    path('breeds/<int:pk>/', views.BreedDetailView.as_view(), name='breed_detail'),
    path('breeds/<int:pk>/update/', views.BreedUpdateView.as_view(), name='breed_update'),
    path('breeds/<int:pk>/delete/', views.BreedDeleteView.as_view(), name='breed_delete'),

    # Хозяева
    path('owners/', views.OwnerListView.as_view(), name='owner_list'),
    path('owners/create/', views.OwnerCreateView.as_view(), name='owner_create'),
    path('owners/<int:pk>/', views.OwnerDetailView.as_view(), name='owner_detail'),
    path('owners/<int:pk>/update/', views.OwnerUpdateView.as_view(), name='owner_update'),
    path('owners/<int:pk>/delete/', views.OwnerDeleteView.as_view(), name='owner_delete'),

    # Ринги
    path('rings/', views.RingListView.as_view(), name='ring_list'),
    path('rings/create/', views.RingCreateView.as_view(), name='ring_create'),
    path('rings/<int:pk>/', views.RingDetailView.as_view(), name='ring_detail'),
    path('rings/<int:pk>/update/', views.RingUpdateView.as_view(), name='ring_update'),
    path('rings/<int:pk>/delete/', views.RingDeleteView.as_view(), name='ring_delete'),

    # Эксперты
    path('experts/', views.ExpertListView.as_view(), name='expert_list'),
    path('experts/create/', views.ExpertCreateView.as_view(), name='expert_create'),
    path('experts/<int:pk>/', views.ExpertDetailView.as_view(), name='expert_detail'),
    path('experts/<int:pk>/update/', views.ExpertUpdateView.as_view(), name='expert_update'),
    path('experts/<int:pk>/delete/', views.ExpertDeleteView.as_view(), name='expert_delete'),
    path('experts/<int:pk>/fire/', views.ExpertFireView.as_view(), name='expert_fire'),
    path('experts/<int:pk>/rehire/', views.ExpertRehireView.as_view(), name='expert_rehire'),
    path('experts/<int:pk>/replace/', views.ExpertReplaceView.as_view(), name='expert_replace'),

    # Медали
    path('medals/', views.MedalListView.as_view(), name='medal_list'),
    path('medals/create/', views.MedalCreateView.as_view(), name='medal_create'),
    path('medals/by-club/', views.medals_by_club, name='medals_by_club'),
    path('medals/record-holders/', views.record_holders, name='record_holders'),
    path('medals/<int:pk>/', views.MedalDetailView.as_view(), name='medal_detail'),
    path('medals/<int:pk>/update/', views.MedalUpdateView.as_view(), name='medal_update'),
    path('medals/<int:pk>/delete/', views.MedalDeleteView.as_view(), name='medal_delete'),

    # Расписания
    path('schedules/', views.ScheduleListView.as_view(), name='schedule_list'),
    path('schedules/create/', views.ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedules/<int:pk>/', views.ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedules/<int:pk>/update/', views.ScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedules/<int:pk>/delete/', views.ScheduleDeleteView.as_view(), name='schedule_delete'),
]