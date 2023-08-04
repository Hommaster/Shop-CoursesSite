from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string

from .orders import OrderItem


class Subject(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Course(models.Model):
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique=True)
    subject = models.ForeignKey(Subject,
                                on_delete=models.CASCADE,
                                related_name='courses')
    owner = models.ForeignKey(User,
                              on_delete=True,
                              related_name='course_owner')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class Module(models.Model):
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='module_owner')
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='modules')
    title = models.CharField(max_length=250)
    description = models.TextField()
    order = OrderItem(for_fields=['course'],
                      blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={
                                         'model__in': (
                                             'text',
                                             'image',
                                             'video',
                                             'file'
                                         )
                                     })
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderItem(for_fields=['module'],
                      blank=True)

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def render(self):
        return render_to_string(
            f"courses/content/{self._meta.model_name}.html",
            {'item': self}
        )

    class Meta:
        abstract = True


class Text(ItemBase):
    content = models.TextField()


class Image(ItemBase):
    file = models.FileField(upload_to='image')


class File(ItemBase):
    file = models.FileField(upload_to='file')


class Video(ItemBase):
    url = models.URLField()
