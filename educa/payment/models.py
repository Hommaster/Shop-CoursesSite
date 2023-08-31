from django.db import models

from courses.models import Course
from accounts.models import Profile


class PaymentCourses(models.Model):
    coursep = models.ForeignKey(Course, on_delete=models.PROTECT,
                                related_name='course_payment')
    profilep = models.ForeignKey(Profile, on_delete=models.PROTECT,
                                 related_name='profile_payment')
    price = models.DecimalField(decimal_places=2,
                                max_digits=10)

    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.coursep.title)
