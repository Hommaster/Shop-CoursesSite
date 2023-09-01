import pytest
from django.contrib.auth.models import User

from ..models import Profile


@pytest.mark.django_db
def test_user_profile_create():
    user = User.objects.create(
        username='User',
        email='user@mail.ru',
        password='31012002sesiD'
    )
    Profile.objects.create(user=user)
    assert Profile.objects.count() == 1
