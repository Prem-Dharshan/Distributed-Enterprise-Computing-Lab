from django.contrib import admin
from django.urls import path, include

from labExam.views import home

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('auth/', include('authentication.urls')),
    path('user/', include('user.urls')),
]
