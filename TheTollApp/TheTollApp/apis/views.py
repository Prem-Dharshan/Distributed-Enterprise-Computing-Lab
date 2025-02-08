# views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login

from decimal import Decimal
from .models import Profile, Transaction
from django.utils.timezone import now
from django.db import transaction as db_transaction

@login_required
def dashboard(request):
    profile = request.user.profile
    transactions = Transaction.objects.filter(profile=profile)
    return render(request, 'dashboard.html', {'profile': profile, 'transactions': transactions})


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

            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

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


## Aparna - a helping hand 

@login_required
def dashboard_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user, defaults={'car_number': 'N/A', 'balance': 0.00})
    
    if request.user.is_superuser:
        return redirect('admin_view')  # Redirect superusers to the admin panel

    transactions = Transaction.objects.filter(profile=profile)
    return render(request, 'dashboard.html', {'profile': profile, 'transactions': transactions})


@login_required
def recharge_view(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])  
        profile = request.user.profile

        with db_transaction.atomic():
            profile.balance += amount
            profile.save()

    return redirect('dashboard')

@login_required
def pay_toll_view(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])  
        profile = request.user.profile

        if profile.balance >= amount:
            with db_transaction.atomic():
                profile.balance -= amount
                profile.save()
                Transaction.objects.create(profile=profile, amt=amount, in_time=now())

    return redirect('dashboard')

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_view(request):
    date_filter = request.GET.get('date')
    user_filter = request.GET.get('user')
    car_number_filter = request.GET.get('car_number')

    transactions = Transaction.objects.select_related('profile').all()

    if date_filter:
        transactions = transactions.filter(in_time__date=date_filter)
    
    if user_filter:
        transactions = transactions.filter(profile__user__username__icontains=user_filter)
    
    if car_number_filter:
        transactions = transactions.filter(profile__car_number__icontains=car_number_filter)

    return render(request, 'admin.html', {'transactions': transactions})

