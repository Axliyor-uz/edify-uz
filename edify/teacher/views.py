from django.shortcuts import render,redirect
from .models import Teacher
from classes.models import Class
# Create your views here.

def teacher_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    elif request.user.role != 'teacher':
        return redirect('accounts:login')
    
    return render(request, 'teacher/dashboard.html', {
        'classes': Class
    })
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



def teacher_create_class(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    elif request.user.role != 'teacher':
        return redirect('accounts:login')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')

        teacher = request.user.teacher


        Class.objects.create(
            name=name,
            bio=bio,
            teacher=teacher
        )

        return redirect('teacher:allclasses')
    
    return render(request, "teacher/create_class.html")





def teacher_classes(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    elif request.user.role != 'teacher':
        return redirect('accounts:login')

    teacher = request.user.teacher  # OneToOne relation

    classes = Class.objects.filter(teacher=teacher)

    return render(request, 'teacher/all_classes.html', {
        'classes': classes
    })