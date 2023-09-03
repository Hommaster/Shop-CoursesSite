import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import Course, Subject, Module, Content

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
def test_course_create_url_for_admin_user(client, user):
    client.force_login(user['admin_user'])
    url = reverse('course_create')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_create_url_not_admin(client, user):
    client.force_login(user['user'])
    url = reverse('course_create')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_subject(client, user):
    client.force_login(user['admin_user'])
    subject = Subject.objects.create(title='Python', slug='python')
    assert Subject.objects.count() == 1


@pytest.fixture
def subject(client, user):
    client.force_login(user['admin_user'])
    Subject.objects.create(title='Python', slug='python')
    subject = Subject.objects.get(title='Python')
    return subject


@pytest.fixture
def course(user, subject):
    course = Course.objects.create(
        owner=user['admin_user'],
        title='Course 1',
        slug='course_1',
        subject=subject,
        description='test description',
    )
    return course


@pytest.mark.django_db
def test_course_edit(client, course):
    url = reverse('course_edit', kwargs={'pk': course.id})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_edit_not_auth_user(client, course):
    client.logout()
    url = reverse('course_edit', kwargs={'pk': course.id})
    response = client.get(url)
    """ reverse to 'login' """
    assert response.status_code == 302


@pytest.mark.django_db
def test_course_delete_edit(client, course):
    url = reverse('course_delete', kwargs={'pk': course.id})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_delete_not_auth_user(client, course):
    client.logout()
    url = reverse('course_delete', kwargs={'pk': course.id})
    response = client.get(url)
    """ reverse to 'login' """
    assert response.status_code == 302


@pytest.mark.django_db
def test_mine_course_change(client, course):
    url = reverse('mine_course_change', kwargs={'slug': course.slug})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_mine_course_change_not_auth_user(client, course):
    client.logout()
    url = reverse('mine_course_change', kwargs={'slug': course.slug})
    response = client.get(url)
    """ reverse to 'login' """
    assert response.status_code == 302


@pytest.mark.django_db
def test_course_detail(client, course, subject):
    url = reverse('course_detail', kwargs={'slug': course.slug})
    Subject.objects.get()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_course_list(client):
    url = reverse('course_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_module(client, course):
    Module.objects.create(course=course, title='Module 1', description='Module')
    assert Module.objects.count() == 1


@pytest.fixture
def module(course):
    Module.objects.create(course=course, title='Module 1', description='Module')
    module = Module.objects.get(course=course)
    return module


@pytest.mark.django_db
def test_course_module_update(client, user, course):
    url = reverse('course_module_update', kwargs={'pk': course.id})
    response = client.get(url)
    assert response.status_code == 200
