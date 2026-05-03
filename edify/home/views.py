from django.shortcuts import render, redirect

def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('student:dashboard')
        elif request.user.role == 'teacher':
            return redirect('teacher:dashboard')
    return render(request, 'home/home.html')