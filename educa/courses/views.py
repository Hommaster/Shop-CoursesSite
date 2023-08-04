from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from django.views.generic.base import TemplateResponseMixin
from django.views import View

from .forms import ModuleFormset



from .models import Course


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owmer=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin,
                       PermissionRequiredMixin):
    model = Course
    fields = ['title', 'subject', 'description']
    success_url = reverse_lazy('manage_course_list')


class OwnerEditCourseMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseUpdateView(OwnerEditCourseMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseCreateView(OwnerEditCourseMixin, CreateView):
    permission_required = 'courses.change_course'


class ModuleCourseUpdateView(TemplateResponseMixin, View):
    course = None
    template_name = 'courses/manage/module/'

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)

    def get_formset(self, data=None):
        return ModuleFormset(instance=self.course, data=data)

    def get(self, request, pk):
        formset = self.get_formset()
        return self.render_to_response(
            {
                'formset': formset,
                'course': self.course
            }
        )

    def post(self, request, pk):
        formset = self.get_formset(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('')
        return self.render_to_response(
            {
                'formset': formset,
                'course': self.course
            }
        )
