from django import forms

from courses.models import Course

from .models import PayCourse


class FromCreatePayCourse(forms.ModelForm):
    class Meta:
        model = PayCourse
        fields = ['price']


class FormPayCourse(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
