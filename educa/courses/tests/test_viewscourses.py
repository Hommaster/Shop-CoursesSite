import pytest
from django.urls import reverse

from pytests.test_father import user, subject, course, module

from ..models import Subject, Module


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


@pytest.mark.django_db
def test_course_module_update(client, user, course):
    url = reverse('course_module_update', kwargs={'pk': course.id})
    response = client.get(url)
    assert response.status_code == 200
