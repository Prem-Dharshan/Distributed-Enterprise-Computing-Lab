from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm
from .models import Category, Todo


@login_required
def create_profile(request):
    if hasattr(request.user, 'profile') and request.user.profile.email:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile created successfully!")
            return redirect('/dashboard/')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'user/create_profile.html', {'form': form})


@login_required
def profile(request):
    user_profile = request.user.profile
    return render(request, 'user/profile.html', {'profile': user_profile})


@login_required
def create_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        priority = request.POST.get('priority')
        due_date = request.POST.get('due_date')
        attachment = request.FILES.get('attachment')

        category = Category.objects.get(id=category_id) if category_id else None

        Todo.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            priority=priority,
            due_date=due_date,
            attachment=attachment
        )
        return redirect('dashboard')

    categories = Category.objects.all()
    return render(request, 'user/create_todo.html', {'categories': categories})


@login_required
def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)

    if todo.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this task.")

    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description')
        category_id = request.POST.get('category')
        todo.priority = request.POST.get('priority')
        todo.due_date = request.POST.get('due_date')

        if request.FILES.get('attachment'):
            todo.attachment = request.FILES.get('attachment')

        todo.category = Category.objects.get(id=category_id) if category_id else None
        todo.save()
        return redirect('dashboard')

    categories = Category.objects.all()
    return render(request, 'user/update_todo.html', {'todo': todo, 'categories': categories})


@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)

    if todo.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this task.")

    if request.method == 'POST':
        todo.delete()
        return redirect('dashboard')

    return render(request, 'user/delete_todo.html', {'todo': todo})
