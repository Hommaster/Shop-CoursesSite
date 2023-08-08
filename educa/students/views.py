from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from courses.models import Course
from accounts.models import Profile

from .forms import EnrollStudentForm


class StudentCourseMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseListView(LoginRequiredMixin,
                            StudentCourseMixin,
                            ListView):
    template_name = 'students/course/list.html'
    model = Course


class StudentCourseDetailView(LoginRequiredMixin,
                              DetailView,
                              StudentCourseMixin):
    template_name = 'students/course/detail.html'
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all()
        context['enroll_form'] = EnrollStudentForm(
            initial={
                'course': course,
                'profile': self.request.user
            }
        )
        return context


class StudentRegistration(CreateView):
    form_class = UserCreationForm
    template_name = 'students/student/registration.html'

    def form_valid(self, form):
        resul = self.form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'],
            password=cd['password1']
        )
        login(self.request, user)
        return resul


class StudentEnrollView(LoginRequiredMixin, FormView):
    form_class = EnrollStudentForm
    course = None
    profile = None

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        self.profile = form.cleaned_data['profile']
        self.profile.course.add(self.course)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentUnenrollView(LoginRequiredMixin, FormView):
    form_class = EnrollStudentForm
    course = None
    profile = None

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.profile = form.cleaned_data['profile']
        self.course.students.remove(self.request.user)
        self.profile.course.remove(self.course)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course_list')
