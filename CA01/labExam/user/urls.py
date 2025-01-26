from django.urls import path
from . import views

urlpatterns = [
    path('create-profile/', views.create_profile, name='create_profile'),
    path('profile/', views.profile, name='profile'),
]
