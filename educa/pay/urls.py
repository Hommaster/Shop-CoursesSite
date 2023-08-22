from . import views
from django.urls import path

urlpatterns = [
    path('create_price/<int:pk>/', views.CreatePricePayCourse.as_view(),
         name='pay_create_price'),
]
