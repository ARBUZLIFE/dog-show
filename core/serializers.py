from rest_framework import serializers

from .models import (
    Club, Breed, Owner, Ring,
    Expert, Dog, Medal, RingBreedSchedule,
)


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'full_name', 'passport_data']


class RingSerializer(serializers.ModelSerializer):
    club_name = serializers.CharField(source='club.name', read_only=True)

    class Meta:
        model = Ring
        fields = ['id', 'number', 'address', 'club', 'club_name']


class ExpertSerializer(serializers.ModelSerializer):
    breed_name = serializers.CharField(source='breed.name', read_only=True)
    club_name = serializers.CharField(source='club.name', read_only=True)
    ring_number = serializers.IntegerField(source='ring.number', read_only=True, allow_null=True)

    class Meta:
        model = Expert
        fields = [
            'id', 'full_name',
            'breed', 'breed_name',
            'ring', 'ring_number',
            'club', 'club_name',
            'is_active',
        ]

    def validate(self, data):
        club = data.get('club') or getattr(self.instance, 'club', None)
        ring = data.get('ring') or getattr(self.instance, 'ring', None)
        if club and ring and ring.club_id != club.id:
            raise serializers.ValidationError(
                'Выбранный ринг принадлежит другому клубу.'
            )
        return data


class DogSerializer(serializers.ModelSerializer):
    breed_name = serializers.CharField(source='breed.name', read_only=True)
    club_name = serializers.CharField(source='club.name', read_only=True)
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    medals_count = serializers.IntegerField(source='medals.count', read_only=True)

    class Meta:
        model = Dog
        fields = [
            'id', 'name',
            'breed', 'breed_name',
            'club', 'club_name',
            'owner', 'owner_name',
            'age', 'pedigree_number', 'parent_names',
            'last_vaccination_date', 'is_disqualified',
            'medals_count',
        ]


class MedalSerializer(serializers.ModelSerializer):
    dog_name = serializers.CharField(source='dog.name', read_only=True)
    breed_name = serializers.CharField(source='breed.name', read_only=True)
    medal_type_display = serializers.CharField(source='get_medal_type_display', read_only=True)

    class Meta:
        model = Medal
        fields = [
            'id', 'dog', 'dog_name',
            'breed', 'breed_name',
            'medal_type', 'medal_type_display',
            'awarded_at',
        ]
        read_only_fields = ['breed']


class RingBreedScheduleSerializer(serializers.ModelSerializer):
    ring_number = serializers.IntegerField(source='ring.number', read_only=True)
    breed_name = serializers.CharField(source='breed.name', read_only=True)

    class Meta:
        model = RingBreedSchedule
        fields = ['id', 'ring', 'ring_number', 'breed', 'breed_name', 'time_slot']