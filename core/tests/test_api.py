import pytest
from django.urls import reverse


def test_api_requires_auth(client):
    response = client.get('/api/v1/dogs/')
    assert response.status_code in (401, 403)


def test_api_dogs_list(client, admin_user, dog):
    client.force_login(admin_user)
    response = client.get('/api/v1/dogs/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == 'Рекс'
    assert data[0]['breed_name'] == 'Немецкая овчарка'


def test_api_create_breed(client, admin_user):
    client.force_login(admin_user)
    response = client.post(
        '/api/v1/breeds/',
        data={'name': 'Такса'},
        content_type='application/json',
    )
    assert response.status_code == 201
    assert response.json()['name'] == 'Такса'

    from core.models import Breed
    assert Breed.objects.filter(name='Такса').exists()


def test_api_disqualify_action(client, admin_user, dog):
    client.force_login(admin_user)
    response = client.post(f'/api/v1/dogs/{dog.pk}/disqualify/')
    assert response.status_code == 200

    dog.refresh_from_db()
    assert dog.is_disqualified is True


def test_api_restore_action(client, admin_user, dog):
    dog.is_disqualified = True
    dog.save()

    client.force_login(admin_user)
    response = client.post(f'/api/v1/dogs/{dog.pk}/restore/')
    assert response.status_code == 200

    dog.refresh_from_db()
    assert dog.is_disqualified is False


def test_api_medals_by_club(client, admin_user, medal):
    client.force_login(admin_user)
    response = client.get('/api/v1/medals/by_club/')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['club_name'] == 'Верный друг'
    assert data[0]['gold'] == 1