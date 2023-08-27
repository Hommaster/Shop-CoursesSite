from django import forms

from courses.models import Course

from .models import PayCourse


class FromCreatePayCourse(forms.Form):
    price = forms.DecimalField()


class FormPayCourse(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
