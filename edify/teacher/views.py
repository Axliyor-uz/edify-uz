from django.shortcuts import render,redirect,get_object_or_404
from student.models import Student
from classes.models import Class
from classes.models import Membership
from django.contrib import messages
from collections import defaultdict
from django.utils import timezone


# Create your views here.

def teacher_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return redirect('accounts:login')
    
    
    teacher = request.user.teacher

    total_students = Student.objects.filter(
        memberships__class_obj__teacher=teacher
    ).distinct().count()


    total_classes = Class.objects.filter(
        teacher=request.user.teacher
    ).count()

    today = timezone.now().date()

    today_students_count = Membership.objects.filter(
        class_obj__teacher=request.user.teacher,
        date_joined=today
    ).count()

    return render(request, 'teacher/dashboard.html', {
        'total_classes': total_classes , 'total_students':total_students, 
        'last_joined': today_students_count
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






def teacher_assignments(request):
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return redirect('accounts:login')
    
    return render(request, 'teacher/assignments.html')






def teacher_students(request):
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return redirect('accounts:login')

    teacher = request.user.teacher

    memberships = Membership.objects.filter(
        class_obj__teacher=teacher
    ).select_related('student__user', 'class_obj')

    # 🔥 group by student
    student_classes = defaultdict(list)

    for m in memberships:
        student_classes[m.student].append(m.class_obj)

    context = {
        'student_classes': dict(student_classes)
    }

    return render(request, 'teacher/students.html', context)






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

    teacher = request.user.teacher

    if request.method == "POST":
        # get form data
        username = request.POST.get("username")
        email = request.POST.get("email")
        uname = request.POST.get("uname")
        bio = request.POST.get("bio")

        # update User model
        request.user.username = username
        request.user.email = email
        request.user.save()

        # update Teacher model
        teacher.uname = uname
        teacher.bio = bio
        teacher.save()

        messages.success(request, "Profile updated successfully!")

        return redirect("teacher:settings")

    return render(request, "teacher/settings.html")






def edit_class(request, class_id):
    cls = get_object_or_404(Class, id=class_id)

    if request.method == "POST":
        cls.name = request.POST.get("name")
        cls.bio = request.POST.get("bio")
        cls.save()
        return redirect('teacher:allclasses')

    return render(request, "teacher/edit_class.html", {"class": cls})

    



