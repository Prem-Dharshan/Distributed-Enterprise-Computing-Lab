from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm


@login_required
def create_profile(request):
    # Check if user already has a profile completed
    if hasattr(request.user, 'profile') and request.user.profile.email:
        return redirect('dashboard')  # Redirect to dashboard if profile is complete

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile created successfully!")
            return redirect('dashboard')  # Redirect to dashboard after saving
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'user/create_profile.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'user/profile.html', {'profile': profile})
