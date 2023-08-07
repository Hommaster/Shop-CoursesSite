from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.forms import modelform_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView

from django.views.generic.base import TemplateResponseMixin
from django.views import View

from .forms import ModuleFormset
from .models import Course, Module, Content, Subject

from braces.views import CsrfExemptMixin, JSONResponseMixin

from students.forms import EnrollStudentForm


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin,
                       PermissionRequiredMixin):
    model = Course
    fields = ['title', 'slug', 'subject', 'description']
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
    template_name = 'courses/manage/module/formset.html'

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
            return redirect('manage_course_list')
        return self.render_to_response(
            {
                'formset': formset,
                'course': self.course
            }
        )


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/contents/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'image', 'file', 'video']:
            return apps.get_model(app_label='course',
                                  model_name=model_name)

    def get_formset(self, model, *args, **kwargs):
        form = modelform_factory(model,
                                 exclude=[
                                     'owner',
                                     'created',
                                     'updated',
                                     'order',
                                 ])
        return form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_formset(self.model,
                                instance=self.obj)
        return self.render_to_response(
            {
                'form': form,
                'obj': self.obj
            }
        )

    def post(self, request, module_id, model_name, id=None):
        form = self.get_formset(self.model,
                                instance=self.obj,
                                data=request.POST,
                                files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module,
                                       item=obj)
            return redirect('module_content_lis', self.module.id)
        return self.render_to_response(
            {
                'form': form,
                'obj': self.obj
            }
        )


class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.items.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response(
            {
                'module': module
            }
        )


class ModuleOrderEdit(CsrfExemptMixin,
                      JSONResponseMixin,
                      View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response(
            {
                'status': 'OK'
            }
        )


class ContentOrderEdit(CsrfExemptMixin,
                       JSONResponseMixin,
                       View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)


class CourseListView(TemplateResponseMixin, View):
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(
            total_courses=Count('courses')
        )
        courses = Course.objects.annotate(
            total_module=Count('modules')
        )
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response(
            {
                'subjects': subjects,
                'subject': subject,
                'courses': courses
            }
        )


class CourseDetailView(DetailView):
    template_name = 'courses/course/detail.html'
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_course'] = EnrollStudentForm(
            initial={
                'course': self.object
            }
        )
        return context
