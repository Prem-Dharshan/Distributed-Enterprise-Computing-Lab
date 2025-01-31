from django.urls import path
from . import views
from .views import create_todo, update_todo, delete_todo

urlpatterns = [
    path('create-profile/', views.create_profile, name='create_profile'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/create/', create_todo, name='create_todo'),
    path('dashboard/update/<int:todo_id>/', update_todo, name='update_todo'),
    path('dashboard/delete/<int:todo_id>/', delete_todo, name='delete_todo'),
]
