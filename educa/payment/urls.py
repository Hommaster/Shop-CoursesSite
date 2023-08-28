from . import views
from django.urls import path


app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process,
         name='payment_process'),
    path('completed/', views.payment_completed,
         name='completed'),
    path('canceled/', views.payment_canceled,
         name='canceled'),
]
