import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import PayCourse

from pytests.test_father import user, subject, course


@pytest.mark.django_db
def test_create_pay_course(client, course):
    PayCourse.objects.create(course=course, price=200)
    assert PayCourse.objects.count() == 1


@pytest.mark.django_db
def test_forwarding_pay_course_url(client, course):
    url = reverse('forwarding_pay_course', kwargs={'course_slug': course.slug})
    response = client.get(url)
    assert response.status_code == 200
