from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProfileSerializer, RegistrationSerializer


class RegistrateApi(APIView):
    def get(self):
        serializer = RegistrationSerializer()
        return Response(serializer.data)