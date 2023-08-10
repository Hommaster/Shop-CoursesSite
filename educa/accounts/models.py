from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from courses.models import Course
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    course = models.ManyToManyField(Course,
                                    related_name='courses',
                                    blank=True)
    slug = models.SlugField()
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username) + '-' + str(self.user.id)
            super(Profile, self).save(*args, **kwargs)
