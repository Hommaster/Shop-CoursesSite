from django.forms import inlineformset_factory
from .models import Course, Module
from django import forms


ModuleFormset = inlineformset_factory(Course,
                                      Module,
                                      fields=['title', 'description'],
                                      extra=2,
                                      can_delete=True)


class CourseForm(forms.ModelForm):

    class Meta:
        fields = ['title', 'subject', 'description']
