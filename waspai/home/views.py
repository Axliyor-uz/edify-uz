from django.shortcuts import render, redirect

def home_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('accounts:profile')
        elif request.user.role == 'teacher':
            return redirect('accounts:profile')
        
    return render(request, 'home/home.html')