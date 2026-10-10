from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend

from .api_permissions import IsOrganizerOrReadOnly, IsStaffOrReadOnly

from .models import (
    Club, Breed, Owner, Ring,
    Expert, Dog, Medal, RingBreedSchedule,
)
from .serializers import (
    ClubSerializer, BreedSerializer, OwnerSerializer, RingSerializer,
    ExpertSerializer, DogSerializer, MedalSerializer, RingBreedScheduleSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

class ClubViewSet(BaseViewSet):
    permission_classes = [IsOrganizerOrReadOnly]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']


class BreedViewSet(BaseViewSet):
    permission_classes = [IsOrganizerOrReadOnly]
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    search_fields = ['name']


class OwnerViewSet(BaseViewSet):
    permission_classes = [IsOrganizerOrReadOnly]
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    search_fields = ['full_name', 'passport_data']


class RingViewSet(BaseViewSet):
    permission_classes = [IsOrganizerOrReadOnly]
    queryset = Ring.objects.select_related('club')
    serializer_class = RingSerializer
    search_fields = ['number', 'address']
    ordering_fields = ['number']


class ExpertViewSet(BaseViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Expert.objects.select_related('breed', 'ring', 'club')
    serializer_class = ExpertSerializer
    search_fields = ['full_name']
    filterset_fields = ['breed', 'club', 'is_active']


class DogViewSet(BaseViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Dog.objects.select_related('breed', 'club', 'owner')
    serializer_class = DogSerializer
    search_fields = ['name', 'pedigree_number']
    filterset_fields = ['breed', 'club', 'owner', 'is_disqualified']

    @action(detail=True, methods=['post'])
    def disqualify(self, request, pk=None):
        dog = self.get_object()
        dog.is_disqualified = True
        dog.save(update_fields=['is_disqualified'])
        return Response({'status': 'disqualified', 'dog_id': dog.id})

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        dog = self.get_object()
        dog.is_disqualified = False
        dog.save(update_fields=['is_disqualified'])
        return Response({'status': 'restored', 'dog_id': dog.id})


class MedalViewSet(BaseViewSet):
    permission_classes = [IsOrganizerOrReadOnly]
    queryset = Medal.objects.select_related('dog', 'breed')
    serializer_class = MedalSerializer
    filterset_fields = ['medal_type', 'breed', 'dog']
    ordering_fields = ['awarded_at']

    @action(detail=False, methods=['get'])
    def by_club(self, request):
        rows = (
            Club.objects
            .annotate(
                gold=Count('dogs__medals', filter=Q(dogs__medals__medal_type='gold')),
                silver=Count('dogs__medals', filter=Q(dogs__medals__medal_type='silver')),
                bronze=Count('dogs__medals', filter=Q(dogs__medals__medal_type='bronze')),
            )
        )
        data = [
            {
                'club_id': c.id,
                'club_name': c.name,
                'gold': c.gold,
                'silver': c.silver,
                'bronze': c.bronze,
                'total': c.gold + c.silver + c.bronze,
            }
            for c in rows
        ]
        return Response(data)


class RingBreedScheduleViewSet(BaseViewSet):
    permission_classes = [IsOrganizerOrReadOnly]
    queryset = RingBreedSchedule.objects.select_related('ring', 'breed')
    serializer_class = RingBreedScheduleSerializer
    filterset_fields = ['ring', 'breed']