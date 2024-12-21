from django.urls import path

from . import views
from .views import booking_detail_view, all_bookings_view

urlpatterns = [
    path('<int:id>/', booking_detail_view, name='booking-detail'),
    path('all/', all_bookings_view, name='all-bookings')
]