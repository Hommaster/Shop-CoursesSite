from django.conf import settings
from django.db import models

from courses.models import Course


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    course = models.ManyToManyField(Course,
                                    related_name='courses',
                                    blank=True,
                                    null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.user.username
