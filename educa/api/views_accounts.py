from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import RegistrationSerializer
from .custom_permissions import IsNotAuthenticated

from accounts.models import Profile


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
