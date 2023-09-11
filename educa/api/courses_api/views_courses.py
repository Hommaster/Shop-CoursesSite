from rest_framework import generics
from courses.models import Course

from .serializers_courses import CourseSerializer


class CourseView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
