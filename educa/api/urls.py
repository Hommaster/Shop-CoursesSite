from django.urls import path
from . import views_courses, views_accounts


urlpatterns = [
    path('', views_courses.CourseView.as_view(), name='api'),
    path('registrate/', views_accounts.RegistrateApi.as_view(), name='registrate_api')
]
