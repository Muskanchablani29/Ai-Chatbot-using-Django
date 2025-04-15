# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm

def Profile(request):
    return render(request, 'Profile.html', {
        "signup_form": SignUpForm(),
        "login_form": LoginForm(),
    })

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your account has been created.")
            return redirect("Home:Home")
        else:
            messages.error(request, "Please correct the errors below")
    return render(request, 'Profile.html', {
        "signup_form": form if request.method == "POST" else SignUpForm(),
        "login_form": LoginForm(),
    })

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("Home:Home")  # Changed to use proper URL namespace
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'Profile.html', {
        "signup_form": SignUpForm(),
        "login_form": form if request.method == "POST" else LoginForm(),
    })

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('Home:Home')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('Home:Home')
    return render(request, 'Profile/confirm_delete.html')
