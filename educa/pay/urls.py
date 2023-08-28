from . import views
from django.urls import path

urlpatterns = [
    path('forwarding/<slug:course_slug>/', views.forwarding_pay_course,
         name='forwarding_pay_course'),
]
