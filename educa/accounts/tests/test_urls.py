import pytest
from django.contrib.auth.models import User

from django.urls import reverse

from ..models import Profile


@pytest.mark.django_db
def test_registrate_url(client):
    url = reverse('registrate')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_url(client):
    url = reverse('edit')
    response = client.get(url)
    """ reverse to 'login' """
    assert response.status_code == 302


@pytest.mark.django_db
def test_profile_view_url(client):
    user = User.objects.create(username='user', password='password', email='email@mail.ru')
    Profile.objects.create(user=user)
    profile = Profile.objects.get(user=user)
    client.force_login(user)
    url = reverse('profile_view', kwargs={'slug': profile.slug})
    response = client.get(url)
    assert response.status_code == 200

    url = reverse('edit')
    response = client.get(url)
    assert response.status_code == 200
