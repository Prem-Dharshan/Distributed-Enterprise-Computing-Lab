from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# Sign-up view
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "User created successfully!")
            return redirect('signin')
        except:
            messages.error(request, "Username already exists!")
            return redirect('signup')

    return render(request, 'authentication/signup.html')


# Sign-in view
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            messages.error(request, "Username and password are required.", extra_tags='signin_error')
            return redirect('signin')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if not hasattr(user, 'profile') or not user.profile.email:
                return redirect('create_profile')

            messages.success(request, "Welcome, you are now logged in!", extra_tags='signin_success')
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.", extra_tags='signin_error')
            return redirect('signin')

    return render(request, 'authentication/signin.html')


def signout(request):
    logout(request)
    messages.info(request, "You have been logged out!")
    return redirect('signin')


@login_required
def dashboard(request):
    return render(request, 'authentication/dashboard.html')
