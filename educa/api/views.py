from rest_framework import generics
from courses.modules import Course

from .serializers import CourseSerializer


class CourseView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
