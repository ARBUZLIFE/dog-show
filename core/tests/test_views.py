import pytest
from django.urls import reverse


def test_home_available_for_anonymous(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'Выставка собак' in response.content.decode()


def test_dog_list_requires_login(client):
    response = client.get(reverse('dog_list'))
    assert response.status_code == 302
    assert '/accounts/login/' in response.url


def test_home_available_for_logged_in(client, user):
    client.force_login(user)
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'Выставка собак' in response.content.decode()


def test_dog_list_shows_dogs(client, user, dog):
    client.force_login(user)
    response = client.get(reverse('dog_list'))
    assert response.status_code == 200
    assert 'Рекс' in response.content.decode()


def test_dog_create_via_post(client, user, breed, club, owner):
    client.force_login(user)
    response = client.post(reverse('dog_create'), data={
        'name': 'Шарик',
        'breed': breed.id,
        'club': club.id,
        'owner': owner.id,
        'age': 2,
        'pedigree_series': '999',
        'pedigree_year': '2023',
        'parent_names': 'П / М',
        'last_vaccination_date': '2025-01-01',
    })
    assert response.status_code == 302

    from core.models import Dog
    assert Dog.objects.filter(name='Шарик').exists()


def test_dog_detail_page(client, user, dog):
    client.force_login(user)
    response = client.get(reverse('dog_detail', args=[dog.pk]))
    assert response.status_code == 200
    content = response.content.decode()
    assert 'Рекс' in content
    assert 'Иванов Иван Иванович' in content  # хозяин


def test_dog_delete(client, user, dog):
    client.force_login(user)
    response = client.post(reverse('dog_delete', args=[dog.pk]))
    assert response.status_code == 302

    from core.models import Dog
    assert not Dog.objects.filter(pk=dog.pk).exists()


def test_medals_by_club_report(client, user, medal):
    client.force_login(user)
    response = client.get(reverse('medals_by_club'))
    assert response.status_code == 200
    assert 'Золото' in response.content.decode()


def test_record_holders_report(client, user, medal):
    client.force_login(user)
    response = client.get(reverse('record_holders'))
    assert response.status_code == 200
    content = response.content.decode()
    assert 'Рекс' in content