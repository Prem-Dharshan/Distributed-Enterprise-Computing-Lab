# Setting Up a Django Project  

### 1. Create and activate a virtual environment (optional but recommended)  
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### 2. Install Django  
```sh
pip install django
```

### 3. Create a Django project  
```sh
django-admin startproject <project_name>
cd <project_name>
```
> If using VS Code, you can open the project with:  
> ```sh
> code .
> ```
> Then, create a virtual environment:  
> ```sh
> python -m venv env
> ```
> Activate it:  
> ```sh
> source env/bin/activate  # On Windows use `env\Scripts\activate`
> ```

### 4. Apply initial migrations  
```sh
python manage.py migrate
```

### 5. Run the development server  
```sh
python manage.py runserver
```
> If you see the Django welcome page at `http://127.0.0.1:8000/`, everything is set up correctly.

---

## Authentication Setup  

### 6. Define Login, Logout, and Redirect URLs in `settings.py`  
Add the following to your `settings.py` file:  
```python
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
```

---

## App Setup  

### 7. Create an app within the project  
```sh
python manage.py startapp <app_name>
```

### 8. Add the app to `INSTALLED_APPS` in `settings.py`  
```python
INSTALLED_APPS = [
    ...
    '<app_name>',
]
```

---

## Include Admin and App Urls with Login redirection

```python
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def redirect_to_login(request):
    return redirect('login')


urlpatterns = [
    path('', redirect_to_login, name='home'),
    path('admin/', admin.site.urls),
    path('', include('todo.urls')), # Include your app urls here, todo is an example
]
```

## MVC Structure


### Models

Goto `models.py` in your app and define your models like this (in this case, a profile and todo model):

```python
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

We are using the default User model provided by Django for authentication.

#### Register the models in the admin panel

Goto `admin.py` in your app and register the models like this:

```python
from django.contrib import admin
from todo.models import Profile, Todo

admin.site.register(Profile)
admin.site.register(Todo)
```

### Views, Forms, Templates and URLs

We are going to build it feature wise
1. Sign up
2. Login
3. Logout
4. Profile
5. Todo
6. Dashboard

#### Sign up View

Create a `views.py` file in your app and define your views like this:

```python
# Sign Up
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Todo
from .forms import UserSignUpForm, ProfileForm, TodoForm
from django.db.models import Count
import json

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
```

Ensure proper imports and replace the form names with your actual form names.

We are using a form to handle user sign up. You can define your form in a `forms.py` file in your app like this:

```python
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Todo

class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
```

We can't simply use the signup template directly, we need a base template to extend from. Create a `base.html` file in your `templates` folder and define your base template like this:

Base Template: Create this file in `templates/base.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}To-Do App{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; padding: 20px; }
        nav { background: #007bff; padding: 10px; color: white; text-align: center; }
        nav a { color: white; margin: 10px; text-decoration: none; }
        .container { max-width: 800px; margin: auto; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background: #007bff; color: white; }
        button { padding: 5px 10px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>

    <nav>
        <a href="{% url 'dashboard' %}">Dashboard</a>
        <a href="{% url 'logout' %}">Logout</a>
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

</body>
</html>
```

Now, create a `signup.html` file in your `templates/auth` folder and define your sign up template like this:
```html
{% extends 'base.html' %}
{% block title %}Sign Up{% endblock %}

{% block content %}
    <h2>Sign Up</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Sign Up</button>
    </form>
    <p>Already have an account? <a href="{% url 'login' %}">Log In</a></p>
{% endblock %}
```

Sign up view is ready. Now, we need to define the URL for the sign up view. Create a `urls.py` file in your app and define your URLs like this:

```python
from django.urls import path
from .views import (
    signup_view
)

urlpatterns = [
    path('signup/', signup_view, name='signup'),
]
```
We'll add more views, forms, templates, and URLs in the same way.

#### Login View

In the `views.py` file in your app and define your login view like this (below the sign up view):

```python
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
```

TBC... 😴
