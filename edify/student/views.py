from django.shortcuts import render, redirect

# Create your views here.

def student_dashboard(request):
    if not request.user.is_authenticated:
            return redirect('accounts:login')
    if request.user.role != 'student':
          return redirect('account:login')
    
    return render(request, 'student/dashboard.html')
