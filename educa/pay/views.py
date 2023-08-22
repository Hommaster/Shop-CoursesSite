from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .models import PayCourse
from .forms import FromCreatePayCourse, FormPayCourse


@login_required
def forwarding_pay_course(request, course):
    pc = PayCourse.objects.create(course=course)
    return reverse_lazy('pay_create_price', args=[pc.id])

# class ForwardingPayCourse(LoginRequiredMixin, FormView):
#     form_class = FormPayCourse
#     course = None
#     pc = None
#
#     def form_valid(self, form):
#         self.course = form.cleaned_data['course']
#         self.pc = PayCourse.objects.create(course=self.course)
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('pay_create_price', args=[self.pc.id])


class CreatePricePayCourse(CreateView):
    template_name = 'pay/create_process.html'
    form_class = FromCreatePayCourse
    pay_course = None

    def form_valid(self, form):
        cd = form.cleaned_data['price']
        self.pay_course = PayCourse.objects.add(price=cd)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course_detail', args=[self.pay_course.course.slug])
