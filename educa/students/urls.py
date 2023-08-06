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
    path('registrate/', views.StudentRegistration.as_view(),
         name='student_registration'),
    path('enroll-course/', views.StudentEnrollView.as_view(),
         name='student_enroll_course')

]
