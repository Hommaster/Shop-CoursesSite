from . import views
from django.urls import path


app_name = 'chat'

urlpatterns = [
    path('room/<course_id>/', views.course_chat_room,
         name='course_chat_room'),
]
