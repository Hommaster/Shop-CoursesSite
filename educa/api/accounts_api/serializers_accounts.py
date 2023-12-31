from django.contrib.auth.models import User
from rest_framework import serializers

from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'course', 'date_of_birth', 'photo']


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, label='password')
    password2 = serializers.CharField(write_only=True, label='password2')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password', 'password2']

    def save(self, *args, **kwargs):
        user = User.objects.create(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: 'Пароль не совпадает'})
        user.set_password(password)
        user.save()
        return user


class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']
        # read_only_fields = ['username', 'email', 'password']


class ProfileEditSerializer(serializers.ModelSerializer):
    user = UserEditSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'date_of_birth', 'photo']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'date_of_birth', 'photo', 'course']
