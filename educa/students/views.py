from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from courses.models import Course
from accounts.models import Profile
from pay.models import PayCourse
from payment.models import Payment

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
                'user': self.request.user
            }
        )
        return context


class StudentEnrollView(LoginRequiredMixin, FormView):
    form_class = EnrollStudentForm
    course = None
    user = None
    profile = None
    pay_course = None

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        if self.course.status is 'F':
            self.course.students.add(self.request.user)
            self.user = form.cleaned_data['user']
            self.profile = Profile.objects.get(user=self.user)
            self.profile.course.add(self.course)
            return super().form_valid(form)
        else:
            self.user = form.cleaned_data['user']
            self.profile = Profile.objects.get(user=self.user)
            self.request.session['profile_id'] = self.profile.id
            self.request.session['course_id'] = self.course.id
            self.pay_course = PayCourse.objects.get(course=self.course)
            payment = Payment()
            payment.course_payment = self.course
            payment.profile_payment = self.profile
            payment.price = self.pay_course.price
            payment.save()
            self.request.session['payment_id'] = payment.id
            return redirect('payment:process')

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentUnenrollView(LoginRequiredMixin, FormView):
    form_class = EnrollStudentForm
    course = None
    profile = None
    user = None

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.remove(self.request.user)
        self.user = form.cleaned_data['user']
        self.profile = Profile.objects.get(user=self.user)
        self.profile.course.remove(self.course)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course_list')
