from django.contrib import admin
from .models import (
    Club, Breed, Owner, Ring,
    Expert, Dog, Medal, RingBreedSchedule,
)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'passport_data')
    search_fields = ('full_name', 'passport_data')


@admin.register(Ring)
class RingAdmin(admin.ModelAdmin):
    list_display = ('number', 'address', 'club')
    list_filter = ('club',)
    search_fields = ('address',)


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'breed', 'ring', 'club', 'is_active')
    list_filter = ('is_active', 'club', 'breed')
    search_fields = ('full_name',)


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'owner', 'club', 'age', 'is_disqualified')
    list_filter = ('breed', 'club', 'is_disqualified')
    search_fields = ('name', 'pedigree_number')


@admin.register(Medal)
class MedalAdmin(admin.ModelAdmin):
    list_display = ('dog', 'breed', 'medal_type', 'awarded_at')
    list_filter = ('medal_type', 'breed')
    search_fields = ('dog__name',)
    exclude = ('breed',) 


@admin.register(RingBreedSchedule)
class RingBreedScheduleAdmin(admin.ModelAdmin):
    list_display = ('ring', 'breed', 'time_slot')
    list_filter = ('ring', 'breed')