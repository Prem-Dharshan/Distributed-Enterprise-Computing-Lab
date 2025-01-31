from django.urls import path
from .views import (
    signup_view, login_view, logout_view, profile_view, dashboard_view, create_todo, update_todo, delete_todo
)

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/create/', create_todo, name='create_todo'),
    path('dashboard/update/<int:todo_id>/', update_todo, name='update_todo'),
    path('dashboard/delete/<int:todo_id>/', delete_todo, name='delete_todo'),
]
