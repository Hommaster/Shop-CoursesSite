from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from courses.models import Course
from accounts.models import Profile


@shared_task
def payment_completed(course_id, profile_id):
    course = get_object_or_404(
        Course,
        id=course_id
    )
    profile = get_object_or_404(
        Profile,
        id=profile_id
    )
    subject = f'Order for {course.title}'
    message = f'Dear {profile.user.username} \n\n' \
              f'You have successfully placed an order.' \
              f'Thanks from {course.owner.username}!'
    mail_send = send_mail(subject, message, 'ilya.pan.2017@gmail.com', [profile.user.email])
    return mail_send
