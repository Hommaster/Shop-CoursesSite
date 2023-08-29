from django.db import models

from courses.models import Course
from accounts.models import Profile


class Payment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING,
                               related_name='course_payment'),
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING,
                                related_name='profile_payment'),
    price = models.DecimalField(decimal_places=2,
                                max_digits=10)

    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.course.title
