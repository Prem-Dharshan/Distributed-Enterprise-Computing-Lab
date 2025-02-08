from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    car_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, to_field='car_number', db_column='car_number')
    amt = models.DecimalField(max_digits=10, decimal_places=2)
    in_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.profile.car_number} - Amount: {self.amt}"

