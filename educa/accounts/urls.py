from . import views
from django.urls import path


urlpatterns = [
    path('registrate/', views.registrate, name='registrate'),
    path('edit/', views.edit, name='edit'),
    # path('profile/<slug:slug>/', views.ProfileView.as_view(),
    #      name='profile_view'),
]
