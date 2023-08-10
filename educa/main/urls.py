from . import views
from django.urls import path

urlpatterns = [
    path('', views.MainPage.as_view(),
         name='home')
]
