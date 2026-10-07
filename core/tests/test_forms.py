import pytest
from datetime import date, timedelta

from core.forms import DogForm


def test_dog_form_valid(db, breed, club, owner):
    form = DogForm(data={
        'name': 'Барсик',
        'breed': breed.id,
        'club': club.id,
        'owner': owner.id,
        'age': 3,
        'pedigree_series': '002',
        'pedigree_year': '2021',
        'parent_names': 'Папа / Мама',
        'last_vaccination_date': '2025-01-01',
        'is_disqualified': False,
    })
    assert form.is_valid(), form.errors


def test_dog_form_invalid_age(db, breed, club, owner):
    form = DogForm(data={
        'name': 'Барсик',
        'breed': breed.id,
        'club': club.id,
        'owner': owner.id,
        'age': 0,
        'pedigree_series': '002',
        'pedigree_year': '2021',
        'parent_names': 'Папа / Мама',
        'last_vaccination_date': '2025-01-01',
    })
    assert not form.is_valid()
    assert 'age' in form.errors


def test_dog_form_future_vaccination(db, breed, club, owner):
    future = (date.today() + timedelta(days=365)).isoformat()
    form = DogForm(data={
        'name': 'Барсик',
        'breed': breed.id,
        'club': club.id,
        'owner': owner.id,
        'age': 3,
        'pedigree_series': '002',
        'pedigree_year': '2021',
        'parent_names': 'Папа / Мама',
        'last_vaccination_date': future,
    })
    assert not form.is_valid()
    assert 'last_vaccination_date' in form.errors


def test_dog_form_series_must_be_digits(db, breed, club, owner):
    form = DogForm(data={
        'name': 'Барсик',
        'breed': breed.id,
        'club': club.id,
        'owner': owner.id,
        'age': 3,
        'pedigree_series': 'abc',
        'pedigree_year': '2021',
        'parent_names': 'Папа / Мама',
        'last_vaccination_date': '2025-01-01',
    })
    assert not form.is_valid()
    assert 'pedigree_series' in form.errors


def test_dog_form_duplicate_pedigree(db, breed, club, owner, dog):
    form = DogForm(data={
        'name': 'Другой',
        'breed': breed.id,
        'club': club.id,
        'owner': owner.id,
        'age': 3,
        'pedigree_series': '001',
        'pedigree_year': '2020',
        'parent_names': 'Папа / Мама',
        'last_vaccination_date': '2025-01-01',
    })
    assert not form.is_valid()
    assert 'pedigree_series' in form.errors