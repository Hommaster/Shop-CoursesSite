import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from pytests.test_father import user, subject, course, module


@pytest.mark.django_db
def test_student_course_list_url(client, user):
    url = reverse('student_course_list')
    client.force_login(user['admin_user'])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_student_course_detail_url(client, course):
    url = reverse('student_course_detail', kwargs={'pk': course.id})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_student_course_detail_module_url(course, module, client):
    url = reverse('student_course_detail_module', kwargs={'pk': course.id, 'module_id': module.id})
    response = client.get(url)
    assert response.status_code == 200
