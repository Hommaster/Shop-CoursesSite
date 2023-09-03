import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import PayCourse

from accounts.models import Profile
from courses.models import Course, Subject


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


@pytest.mark.django_db
def test_create_paycourse(client, course):
    PayCourse.objects.create(course=course, price=200)
    assert PayCourse.objects.count() == 1


@pytest.mark.django_db
def test_forwarding_pay_course_url(client, course):
    url = reverse('forwarding_pay_course', kwargs={'course_slug': course.slug})
    response = client.get(url)
    assert response.status_code == 200
