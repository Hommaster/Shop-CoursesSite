from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView

from django.views.generic.base import TemplateResponseMixin
from django.views import View

from .forms import ModuleFormset, CourseForm
from .models import Course, Module, Content, Subject

from braces.views import CsrfExemptMixin, JSONResponseMixin

from students.forms import EnrollStudentForm
from accounts.models import Profile
from pay.models import PayCourse


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
    fields = ['title', 'subject', 'description']
    success_url = reverse_lazy('manage_course_list')
    permission_required = ''


class OwnerEditCourseMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseUpdateView(OwnerEditCourseMixin, UpdateView):
    permission_required = 'courses.change_course'


class MineCourseUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/course/update.html'
    course = None
    model = None
    obj = None

    def get_form(self, model, *args, **kwargs):
        form = modelform_factory(model=model,
                                 fields=[
                                     'title',
                                     'description',
                                     'status',
                                 ])
        return form(*args, **kwargs)

    def dispatch(self, request, slug):
        try:
            self.course = get_object_or_404(
                Course,
                slug=slug,
                owner=self.request.user
            )
            self.obj = get_object_or_404(Course,
                                         slug=slug,
                                         owner=request.user)
            return super().dispatch(request, slug)
        except TypeError:
            self.course = None
            return redirect('home')
        except Course.DoesNotExist:
            self.course = None
            return redirect('home')

    def get(self, request, slug):
        if self.course:
            form = self.get_form(Course,
                                 instance=self.obj)
            return self.render_to_response(
                {
                    'course': self.course,
                    'form': form
                }
            )
        else:
            return redirect('home')

    def post(self, request, slug):
        form = self.get_form(Course,
                             instance=self.course,
                             data=request.POST)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data['status']
            if cd == self.course.Status.PAY:
                return redirect('forwarding_pay_course', self.course.slug)
            else:
                return redirect('course_detail', self.course.slug)
        else:
            form = self.get_form(Course,
                                 instance=self.course,
                                 data=request.POST)
        return self.render_to_response(
            {
                'course': self.course,
                'form': form,
            }
        )


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseCreateView(OwnerEditCourseMixin, CreateView):
    permission_required = 'courses.add_course'


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
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['tests', 'image', 'file', 'video']:
            return apps.get_model(app_label='courses',
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
            return redirect('module_content_list', self.module.id)
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
        content.item.delete()
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
            total_module=Count('modules'),
            total_students=Count('students_course')
        )
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response(
            {
                'subjects': subjects,
                'subject': subject,
                'courses': courses,
            }
        )


class CourseDetailView(DetailView):
    template_name = 'courses/course/detail.html'
    model = Course
    course = None
    trying = None
    user = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.course = self.object
        self.user = self.request.user
        try:
            Profile.objects.get(user=self.request.user)
            context['reg'] = True
            if self.course.owner.username == self.request.user.username:
                context['owner'] = True
            if self.course.status == 'P':
                context['pay_course'] = get_object_or_404(PayCourse,
                                                          course=self.course)
            else:
                context['pay_course'] = None
            try:
                Profile.objects.filter(course=self.object).get(user=self.request.user)
                context['profile_have_this_course'] = True
            except Profile.DoesNotExist:
                 context['profile_have_this_course'] = False
                 self.trying = False
            if self.trying is False:
                context['enroll_form'] = EnrollStudentForm(
                    initial={
                        'course': self.object,
                        'user': self.user
                    }
                )
                context['enroll'] = True
            else:
                context['enroll'] = False
        except TypeError:
            context['reg'] = False

        return context

