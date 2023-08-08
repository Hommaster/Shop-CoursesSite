from django import forms

from courses.models import Course
from accounts.models import Profile


class EnrollStudentForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
    profile = forms.ModelChoiceField(queryset=Profile.objects.all(),
                                     widget=forms.HiddenInput)
