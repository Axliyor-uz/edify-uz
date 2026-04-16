from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:profile')

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.role == 'student':
                return redirect('student:dashboard')

            elif user.role == 'teacher':
                return redirect('teacher:dashboard')
            
        else:
            error = "Invalid username or password"

    return render(request, 'accounts/login.html', {'error': error})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('students:dashboard')
        elif request.user.role == 'teacher':
            return redirect('teachers:dashboard')
    return render(request, 'home.html')