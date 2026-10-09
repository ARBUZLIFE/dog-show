import pytest
from datetime import date
from django.contrib.auth import get_user_model

from core.models import (
    Club, Breed, Owner, Ring, Expert, Dog, Medal, RingBreedSchedule,
)

User = get_user_model()


# Пользователи

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='tester',
        password='testpass123',
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='admin',
        password='admin12345',
        email='admin@example.com',
    )


# Справочники

@pytest.fixture
def breed(db):
    return Breed.objects.create(name='Немецкая овчарка')


@pytest.fixture
def breed_2(db):
    return Breed.objects.create(name='Пудель')


@pytest.fixture
def club(db):
    return Club.objects.create(name='Верный друг')


@pytest.fixture
def club_2(db):
    return Club.objects.create(name='Московское общество')


@pytest.fixture
def owner(db):
    return Owner.objects.create(
        full_name='Иванов Иван Иванович',
        passport_data='4510 123456',
    )


@pytest.fixture
def ring(db, club):
    return Ring.objects.create(number=1, address='ул. Ленина, 10', club=club)


@pytest.fixture
def expert(db, breed, ring, club):
    return Expert.objects.create(
        full_name='Орлов Виктор Степанович',
        breed=breed,
        ring=ring,
        club=club,
        is_active=True,
    )


@pytest.fixture
def dog(db, breed, club, owner):
    return Dog.objects.create(
        name='Рекс',
        breed=breed,
        club=club,
        owner=owner,
        age=4,
        pedigree_number='РКФ-001-2020',
        parent_names='Цезарь / Альма',
        last_vaccination_date=date(2025, 3, 15),
    )


@pytest.fixture
def medal(db, dog, breed):
    return Medal.objects.create(
        dog=dog,
        medal_type='gold',
        awarded_at=date(2025, 6, 1),
    )


@pytest.fixture
def schedule(db, ring, breed):
    return RingBreedSchedule.objects.create(
        ring=ring,
        breed=breed,
        time_slot='10:00-12:00',
    )