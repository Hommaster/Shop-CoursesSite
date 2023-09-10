from django.contrib.auth.models import User
from rest_framework import serializers

from courses.models import Course
from accounts.models import Profile


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'subject', 'owner', 'description', 'owner', 'students', 'status']


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

    def create(self, validated_data):
        user = super().create(validated_data)
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError('Password not match!')
        user.set_password(validated_data['password'])
        data = validated_data['email']
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError('This email already in use!')
        username = validated_data['username']
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username already in use!')
        user.save()
        return user
