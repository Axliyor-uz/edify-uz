from django.shortcuts import render, redirect
# from .models import Course, Enrollment
# Create your views here.

def student_dashboard(request):
    if not request.user.is_authenticated:
            return redirect('accounts:login')
    if request.user.role != 'student':
          return redirect('accounts:login')
    
    return render(request, 'student/dashboard.html')

def student_courses(request):
    if not request.user.is_authenticated:
            return redirect('accounts:login')
    if request.user.role != 'student':
          return redirect('accounts:login')
    
    return render(request, 'student/courses.html')

def student_teachers(request):
    if not request.user.is_authenticated:
            return redirect('accounts:login')
    if request.user.role != 'student':
          return redirect('accounts:login')
    
    return render(request, 'student/teachers.html')

def student_settings_view(request):
    if not request.user.is_authenticated:
            return redirect('accounts:login')
    if request.user.role != 'student':
          return redirect('accounts:login')
    return render(request, 'student/settings.html')

def student_profile(request):
    if not request.user.is_authenticated:
            return redirect('accounts:login')
    if request.user.role != 'student':
          return redirect('accounts:login')
    
    return render(request, 'student/profile.html')


