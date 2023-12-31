import redis

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

from courses.models import Course
from accounts.models import Profile
from pay.models import PayCourse
from payment.models import PaymentCourses

from .forms import EnrollStudentForm


r = redis.Redis(
    port=settings.REDIS_PORT,
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB,
)


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
        if self.course.status == 'F':
            self.course.students.add(self.request.user)
            self.user = form.cleaned_data['user']
            self.profile = Profile.objects.get(user=self.user)
            self.profile.course.add(self.course)
            r.zincrby('course_rating_enroll', 1, self.course.id)
            return super().form_valid(form)
        else:
            self.user = form.cleaned_data['user']
            self.profile = Profile.objects.get(user=self.user)
            self.pay_course = PayCourse.objects.get(course=self.course)
            payment = PaymentCourses.objects.create(coursep=self.course,
                                                    profilep=self.profile,
                                                    price=self.pay_course.price)
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
