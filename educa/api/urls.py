from django.urls import path
from .courses_api import views_courses
from .accounts_api import views_accounts

urlpatterns = [
    path('', views_courses.CourseView.as_view(), name='api'),
    path('registrate/', views_accounts.RegistrateApi.as_view(), name='registrate_api'),
    path('profile/<slug:slug>/', views_accounts.ProfileDetail.as_view(), name='test_profile'),
    path('edit/<slug:slug>/', views_accounts.ProfileEditAPIView.as_view(), name='edit_api'),
]
