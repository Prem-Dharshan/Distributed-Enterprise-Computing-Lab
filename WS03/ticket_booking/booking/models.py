from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=45)
    detail = models.CharField(max_length=45)
    organizer = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class Show(models.Model):
    start_time = models.DateField()
    end_time = models.DateField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event.name} {self.start_time}"


class Booking(models.Model):
    price = models.FloatField()
    customer = models.CharField(max_length=45)
    capacity = models.FloatField()
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
