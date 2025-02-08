# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True, label="Full Name")
    car_number = forms.CharField(max_length=20, required=True, label="Car Number")

    class Meta(UserCreationForm.Meta):
        model = UserCreationForm.Meta.model
        fields = UserCreationForm.Meta.fields + ("name", "car_number",)

    def save(self, commit=True):
        user = super().save(commit=False)
        name = self.cleaned_data["name"]
        car_number = self.cleaned_data["car_number"]

        if commit:
            user.save()
            profile = Profile(user=user, name=name, car_number=car_number)
            profile.save()

        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'car_number', 'balance']
