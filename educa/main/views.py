from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateResponseMixin, View

from courses.models import Course


class MainPage(ListView):
    template_name = 'main/main_page.html'
    model = Course
