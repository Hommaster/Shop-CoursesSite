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
]
