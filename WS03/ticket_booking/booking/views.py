from django.shortcuts import render, get_object_or_404
from .models import Booking
from .serializers import BookingDetailSerializer


def booking_detail_view(request, id):
    booking = get_object_or_404(Booking, id=id)
    serializer = BookingDetailSerializer(booking)

    return render(request, 'booking/booking_detail.html', {'booking': serializer.data})

def all_bookings_view(request):
    bookings = Booking.objects.all()
    serializer = BookingDetailSerializer(bookings, many=True)

    return render(request, 'booking/all_bookings.html', {'bookings': serializer.data})