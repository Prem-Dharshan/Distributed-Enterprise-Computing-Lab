# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view, dashboard_view, profile_view, update_profile_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile/', profile_view, name='user_profile'),
    path('profile/update/', update_profile_view, name='update_profile'),
]
