import pytest
from django.urls import reverse

from core.models import Dog


def test_home_available_for_anonymous(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'Выставка собак' in response.content.decode()


def test_home_available_for_logged_in(client, user):
    client.force_login(user)
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'Выставка собак' in response.content.decode()


def test_dog_list_requires_login(client):
    response = client.get(reverse('dog_list'))
    assert response.status_code == 302
    assert '/accounts/login/' in response.url


def test_dog_list_shows_dogs(client, user, dog):
    client.force_login(user)
    response = client.get(reverse('dog_list'))
    assert response.status_code == 200
    assert 'Рекс' in response.content.decode()


def test_dog_detail_page(client, user, dog):
    client.force_login(user)
    response = client.get(reverse('dog_detail', args=[dog.pk]))
    assert response.status_code == 200
    content = response.content.decode()
    assert 'Рекс' in content
    assert 'Иванов Иван Иванович' in content


def test_dog_create_via_post(client, organizer_user, breed, club, owner):
    client.force_login(organizer_user)
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
    assert Dog.objects.filter(name='Шарик').exists()


def test_dog_create_by_chairman(client, chairman_user, breed, club, owner):
    client.force_login(chairman_user)
    response = client.post(reverse('dog_create'), data={
        'name': 'Бобик',
        'breed': breed.id,
        'club': club.id,
        'owner': owner.id,
        'age': 3,
        'pedigree_series': '888',
        'pedigree_year': '2022',
        'parent_names': 'П / М',
        'last_vaccination_date': '2025-01-01',
    })
    assert response.status_code == 302
    assert Dog.objects.filter(name='Бобик').exists()


def test_dog_create_by_plain_user_forbidden(client, user, breed, club, owner):
    client.force_login(user)
    response = client.post(reverse('dog_create'), data={
        'name': 'Запрещённый',
        'breed': breed.id,
        'club': club.id,
        'owner': owner.id,
        'age': 2,
        'pedigree_series': '777',
        'pedigree_year': '2023',
        'parent_names': 'П / М',
        'last_vaccination_date': '2025-01-01',
    })
    assert response.status_code == 403


def test_dog_delete(client, organizer_user, dog):
    client.force_login(organizer_user)
    response = client.post(reverse('dog_delete', args=[dog.pk]))
    assert response.status_code == 302
    assert not Dog.objects.filter(pk=dog.pk).exists()


def test_dog_disqualify(client, organizer_user, dog):
    client.force_login(organizer_user)

    response = client.get(reverse('dog_disqualify', args=[dog.pk]))
    assert response.status_code == 200
    assert 'Отстранить' in response.content.decode()

    response = client.post(reverse('dog_disqualify', args=[dog.pk]))
    assert response.status_code == 302

    dog.refresh_from_db()
    assert dog.is_disqualified is True


def test_dog_restore(client, organizer_user, dog):
    dog.is_disqualified = True
    dog.save()

    client.force_login(organizer_user)
    response = client.post(reverse('dog_restore', args=[dog.pk]))
    assert response.status_code == 302

    dog.refresh_from_db()
    assert dog.is_disqualified is False


def test_dog_disqualify_by_chairman(client, chairman_user, dog):
    client.force_login(chairman_user)
    response = client.post(reverse('dog_disqualify', args=[dog.pk]))
    assert response.status_code == 302
    dog.refresh_from_db()
    assert dog.is_disqualified is True


def test_expert_fire(client, chairman_user, expert):
    client.force_login(chairman_user)
    response = client.post(reverse('expert_fire', args=[expert.pk]))
    assert response.status_code == 302
    expert.refresh_from_db()
    assert expert.is_active is False


def test_expert_rehire(client, chairman_user, expert):
    expert.is_active = False
    expert.save()

    client.force_login(chairman_user)
    response = client.post(reverse('expert_rehire', args=[expert.pk]))
    assert response.status_code == 302
    expert.refresh_from_db()
    assert expert.is_active is True


def test_expert_fire_by_organizer_forbidden(client, organizer_user, expert):
    client.force_login(organizer_user)
    response = client.post(reverse('expert_fire', args=[expert.pk]))
    assert response.status_code == 403
    expert.refresh_from_db()
    assert expert.is_active is True


def test_dog_create_with_prefilled_club(client, chairman_user, club, breed, owner):
    client.force_login(chairman_user)
    url = reverse('dog_create') + f'?club={club.pk}'
    response = client.get(url)
    assert response.status_code == 200
    assert 'будет принята в клуб' in response.content.decode()


def test_dog_create_with_club_by_organizer_forbidden(client, organizer_user, club):
    client.force_login(organizer_user)
    url = reverse('dog_create') + f'?club={club.pk}'
    response = client.get(url)
    assert response.status_code == 403


def test_expert_create_with_prefilled_club(client, chairman_user, club):
    client.force_login(chairman_user)
    url = reverse('expert_create') + f'?club={club.pk}'
    response = client.get(url)
    assert response.status_code == 200
    assert 'будет принят в клуб' in response.content.decode()


def test_expert_create_with_club_by_organizer_forbidden(client, organizer_user, club):
    client.force_login(organizer_user)
    url = reverse('expert_create') + f'?club={club.pk}'
    response = client.get(url)
    assert response.status_code == 403


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

def test_organizer_can_create_breed(client, organizer_user):
    client.force_login(organizer_user)
    response = client.get(reverse('breed_create'))
    assert response.status_code == 200


def test_chairman_cannot_create_breed(client, chairman_user):
    client.force_login(chairman_user)
    response = client.get(reverse('breed_create'))
    assert response.status_code == 403


def test_chairman_cannot_create_club(client, chairman_user):
    client.force_login(chairman_user)
    response = client.get(reverse('club_create'))
    assert response.status_code == 403


def test_admin_can_create_breed(client, admin_user):
    client.force_login(admin_user)
    response = client.get(reverse('breed_create'))
    assert response.status_code == 200