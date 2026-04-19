from django.shortcuts import render,redirect
from .models import Teacher
from classes.models import Class
# Create your views here.

def teacher_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    elif request.user.role != 'teacher':
        return redirect('accounts:login')
    
    return render(request, 'teacher/dashboard.html')
def teacher_profile(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    elif request.user.role != 'teacher':
        return redirect('accounts:login')
    
    return render(request, 'teacher/profile.html')
def teacher_settings_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    elif request.user.role != 'teacher':
        return redirect('accounts:login')
    
    return render(request, 'teacher/settings.html')
def teacher_courses(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    elif request.user.role != 'teacher':
        return redirect('accounts:login')
    
    return render(request, 'teacher/courses.html')
def teacher_students(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    elif request.user.role != 'teacher':
        return redirect('accounts:login')
    
    return render(request, 'teacher/students.html')