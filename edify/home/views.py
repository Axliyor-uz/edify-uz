from django.shortcuts import render, redirect

def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('students:dashboard')
        elif request.user.role == 'teacher':
            return redirect('teachers:dashboard')
    return render(request, 'home/home.html')