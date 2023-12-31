from . import views
from django.urls import path


urlpatterns = [
    path('courses/', views.StudentCourseListView.as_view(),
         name='student_course_list'),
    path('course/<pk>/', views.StudentCourseDetailView.as_view(),
         name='student_course_detail'),
    path('course/<pk>/<module_id>/',
         views.StudentCourseDetailView.as_view(),
         name='student_course_detail_module'),
    path('enroll-course/', views.StudentEnrollView.as_view(),
         name='student_enroll_course'),
    path('unenroll-course/', views.StudentUnenrollView.as_view(),
         name='student_unenroll_course'),
]
