import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import Profile


@pytest.fixture
def user():
    admin_user = User.objects.create(username='user', password='password', email='email@mail.ru', is_staff=True, is_superuser=True)
    Profile.objects.create(user=admin_user)
    admin_profile = Profile.objects.get(user=admin_user)
    user = User.objects.create(username='user2', password='password2', email='email2@mail.ru')
    Profile.objects.create(user=user)
    profile = Profile.objects.get(user=user)
    user_profile = {'admin_user': admin_user, 'admin_profile': admin_profile,
                    'user': user, 'profile': profile}
    return user_profile


@pytest.mark.django_db
def test_student_course_list_url(client, user):
    url = reverse('student_course_list')
    client.force_login(user['admin_user'])
    response = client.get(url)
    assert response.status_code == 200
