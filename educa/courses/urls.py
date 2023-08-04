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
]
