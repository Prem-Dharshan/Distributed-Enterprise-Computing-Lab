from django.contrib import admin
from .models import Event, Show, Booking  # Import your models

# Register your models here
admin.site.register(Event)
admin.site.register(Show)
admin.site.register(Booking)
