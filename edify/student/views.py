from django.shortcuts import render, redirect
from classes.models import Membership
from classes.models import Class
from classes.models import Class, Membership
from student.models import Student



def student_dashboard(request):
    if not request.user.is_authenticated:
            return redirect('accounts:login')
    if request.user.role != 'student':
          return redirect('accounts:login')
    
    return render(request, 'student/dashboard.html', {
        'memberships': Membership
    })
  




def student_courses(request):
    if not request.user.is_authenticated:
            return redirect('accounts:login')
    if request.user.role != 'student':
          return redirect('accounts:login')
    
    return render(request, 'student/courses.html')






from django.shortcuts import render, redirect
from classes.models import Membership
from collections import defaultdict

def student_teachers(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.role != 'student':
        return redirect('accounts:login')

    student = request.user.student

    memberships = Membership.objects.filter(
        student=student
    ).select_related('class_obj__teacher__user')

    # group by teacher
    teacher_classes = defaultdict(list)

    for m in memberships:
        teacher = m.class_obj.teacher
        teacher_classes[teacher].append(m.class_obj)

    return render(request, 'student/teachers.html', {
        'teacher_classes': dict(teacher_classes)
    })



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





def student_my_classes(request):

    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.user.role != 'student':
        return redirect('accounts:login')

    student = request.user.student

    enrollments = Membership.objects.filter(student=student).select_related('class_obj')

    return render(request, 'student/my_classes.html', {
        'enrollments': enrollments
    })




def student_all_classes(request):
    if not request.user.is_authenticated:
            return redirect('accounts:login')
    if request.user.role != 'student':
          return redirect('accounts:login')


    classes = Class.objects.all()
    return render(request, 'student/all_classes.html', {'all_classes': classes})





def student_join_class(request, class_id):
    student = request.user.student   # because of OneToOneField

    class_obj = Class.objects.get(id=class_id)

    Membership.objects.get_or_create(
        student=student,
        class_obj=class_obj
    )

    return redirect('student:class', class_id=class_id)





def student_class(request, class_id):
    class_obj = Class.objects.get(id=class_id)


    return render(request, 'student/join_class.html', {
        'classes': class_obj
    })