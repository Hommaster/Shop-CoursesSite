from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView
from django.views.generic.base import TemplateResponseMixin

from .models import PayCourse
from .forms import FromCreatePayCourse, FormPayCourse

from courses.models import Course


@login_required
def forwarding_pay_course(request, course_slug):
    course = get_object_or_404(Course,
                               slug=course_slug)
    if request.method == 'POST':
        PayCourse.objects.create(course=course)
        form = FromCreatePayCourse(request.POST)
        if form.is_valid():
            cd = form.cleaned_data['price']
            pay_course = get_object_or_404(PayCourse,
                                           course=course)
            pay_course.price = cd
            pay_course.save()
            return redirect('course_detail', slug=course.slug)
        else:
            return render(request, 'pay/create_process.html',
                          {
                              'form': form,
                              'course': course
                          })
    else:
        form = FromCreatePayCourse()
        return render(request, 'pay/create_process.html',
                      {
                          'form': form,
                          'course': course,
                      })
