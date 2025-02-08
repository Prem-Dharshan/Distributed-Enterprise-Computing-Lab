# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login

from .forms import SignUpForm, ProfileUpdateForm
from .models import Profile


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)

            return render(request, 'auth/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})


@login_required
def dashboard_view(request):
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'user/profile.html', context)


@login_required
def update_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'user/update_profile.html', context)