from django.db import models

from courses.models import Course


class PayCourse(models.Model):
    course = models.ForeignKey(Course,
                               related_name='pay_course',
                               on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2,
                                max_digits=10,
                                null=True)

    def __str__(self):
        return str(self.id)
