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


def test_dog_disqualify(client, user, dog):
    client.force_login(user)

    # GET — страница подтверждения
    response = client.get(reverse('dog_disqualify', args=[dog.pk]))
    assert response.status_code == 200
    assert 'Отстранить' in response.content.decode()

    # POST — выполняем
    response = client.post(reverse('dog_disqualify', args=[dog.pk]))
    assert response.status_code == 302

    dog.refresh_from_db()
    assert dog.is_disqualified is True


def test_dog_restore(client, user, dog):
    dog.is_disqualified = True
    dog.save()

    client.force_login(user)
    response = client.post(reverse('dog_restore', args=[dog.pk]))
    assert response.status_code == 302

    dog.refresh_from_db()
    assert dog.is_disqualified is False


def test_expert_fire(client, user, expert):
    client.force_login(user)
    response = client.post(reverse('expert_fire', args=[expert.pk]))
    assert response.status_code == 302

    expert.refresh_from_db()
    assert expert.is_active is False


def test_expert_rehire(client, user, expert):
    expert.is_active = False
    expert.save()

    client.force_login(user)
    response = client.post(reverse('expert_rehire', args=[expert.pk]))
    assert response.status_code == 302

    expert.refresh_from_db()
    assert expert.is_active is True


def test_dog_create_with_prefilled_club(client, user, club, breed, owner):
    client.force_login(user)

    # Открываем форму с параметром ?club=X
    url = reverse('dog_create') + f'?club={club.pk}'
    response = client.get(url)
    assert response.status_code == 200
    assert f'будет принята в клуб' in response.content.decode()