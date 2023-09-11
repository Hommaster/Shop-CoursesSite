from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers_accounts import ProfileDetailSerializer, RegistrationSerializer, UserEditSerializer, ProfileEditSerializer

from accounts.models import Profile

from ..custom_permissions import IsNotAuthenticated


class RegistrateApi(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            new_user = serializer.save()
            data['response'] = True
            new_user.save()
            Profile.objects.create(user=new_user)
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data)


class ProfileEditAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'slug'
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileEditSerializer


class ProfileDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileDetailSerializer
