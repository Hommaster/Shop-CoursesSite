from django.urls import path
from . import views


urlpatterns = [
    path('mine/', views.ManageCourseListView.as_view(),
         name='manage_course_list'),
    path('change/<pk>/', views.CourseUpdateView.as_view(),
         name='course_change'),
    path('delete/<pk>/', views.CourseDeleteView.as_view(),
         name='course_delete'),
    path('create/', views.CourseCreateView.as_view(),
         name='course_create'),
    path('edit/<pk>/', views.ModuleCourseUpdateView.as_view(),
         name='course_edit'),
    path('module/<int:module_id>/content/<model_name>/create/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_update'),
    path('module/content/delete/<id>/', views.ContentDeleteView.as_view(),
         name='content_delete'),
    path('module/content/<int:module_id>/', views.ModuleContentListView.as_view(),
         name='content_list'),
    path('module/order/', views.ModuleOrderEdit.as_view(),
         name='module_order'),
    path('content/order/', views.ContentOrderEdit.as_view(),
         name='content_order'),
    path('subject/<slug:subject>/', views.CourseListView.as_view(),
         name='course_list_subject'),
    path('<slug:slug>/', views.CourseDetailView.as_view(),
         name='course_detail'),
]
