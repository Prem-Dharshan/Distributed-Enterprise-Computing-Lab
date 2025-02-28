from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Transaction

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Transaction)
