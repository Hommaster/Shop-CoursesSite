from . import views
from django.urls import path


urlpatterns = [
    path('registrate/', views.registrate, name='registrate'),
    path('edit/', views.edit, name='edit'),
]
