import pytest
from datetime import date

from core.models import Medal


def test_club_str(club):
    assert str(club) == 'Верный друг'


def test_dog_str(dog):
    assert str(dog) == 'Рекс (Немецкая овчарка)'


def test_medal_auto_fills_breed(db, dog, breed):
    medal = Medal.objects.create(
        dog=dog,
        medal_type='gold',
        awarded_at=date(2025, 6, 1),
    )
    assert medal.breed_id == breed.id


def test_medal_breed_auto_corrected(db, dog, breed, breed_2):
    medal = Medal.objects.create(
        dog=dog,
        breed=breed_2,
        medal_type='gold',
        awarded_at=date(2025, 6, 1),
    )
    assert medal.breed_id == breed.id


def test_medal_type_display(medal):
    assert medal.get_medal_type_display() == 'Золото'


def test_ring_str(ring):
    assert 'Ринг №1' in str(ring)


def test_expert_str(expert):
    assert str(expert) == 'Орлов Виктор Степанович'