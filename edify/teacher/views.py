from django.shortcuts import render,redirect
from .models import Teacher
from student.models import Student
from classes.models import Class
from classes.models import Membership
from django.contrib import messages
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
    
    teacher = request.user.teacher

    students = Student.objects.filter(
        memberships__class_obj__teacher=teacher
    ).distinct()


    return render(request, 'teacher/students.html', {'students':students})



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


def teacher_settings(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user = request.user
    teacher = user.teacher

    teacher = getattr(user, 'teacher', None)

    if teacher is None:
        return redirect('teacher:dashboard')  # or create one


    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.teacher.bio = request.POST.get('bio')
        user.teacher.uname = request.POST.get('uname')

        user.save()
        teacher.save

        return redirect('teacher:profile')

    return render(request, 'teacher/settings.html')

    