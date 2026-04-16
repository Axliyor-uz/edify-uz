from django.shortcuts import render,redirect

# Create your views here.

def teacher_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    elif request.user.role != 'teacher':
        return redirect('account:login')
    
    return render(request, 'teacher/dashboard.html')
