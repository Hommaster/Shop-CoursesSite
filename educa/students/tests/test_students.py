import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from ..forms import EnrollStudentForm

from accounts.models import Profile
from courses.models import Course, Subject, Module


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


@pytest.fixture
def module(course):
    Module.objects.create(course=course, title='Module 1', description='Module')
    module = Module.objects.get(course=course)
    return module

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
