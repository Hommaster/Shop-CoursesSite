from django import forms
from django.contrib.auth.models import User

from .models import Profile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Этот адрес электронной почты уже занят!')
        return data


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        cd = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=cd)
        if qs.exists():
            raise forms.ValidationError('Этот адрес электронной почты уже занят!')
        return cd


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
