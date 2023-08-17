from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('room/<int:course_id>/', views.course_chat_room,
         name='course_chat_room'),
    path('room/module/<int:module_id>/',
         views.module_chat_room, name='module_chat_room')
]
