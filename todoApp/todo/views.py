from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Todo
from .forms import UserSignUpForm, ProfileForm, TodoForm
from django.db.models import Count
import json


# Sign Up
def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('profile')
    else:
        form = UserSignUpForm()
    return render(request, 'auth/signup.html', {'form': form})


# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid username or password'})

    return render(request, 'auth/login.html')


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# Profile (Mandatory After Login)
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})


# Dashboard (List Todos + Pie Chart)
@login_required
def dashboard_view(request):
    todos = Todo.objects.filter(user=request.user)

    # Pie chart data
    stats = todos.values('is_completed').annotate(count=Count('id'))
    stats_json = json.dumps(list(stats))

    return render(request, 'dashboard.html', {'todos': todos, 'stats_json': stats_json})


# CRUD Views
@login_required
def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('dashboard')
    else:
        form = TodoForm()
    return render(request, 'todo/create_todo.html', {'form': form})


@login_required
def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/update_todo.html', {'form': form})


@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('dashboard')
    return render(request, 'todo/delete_todo.html', {'todo': todo})
