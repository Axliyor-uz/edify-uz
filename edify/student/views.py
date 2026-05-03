# <<<<<<< HEAD
from django.shortcuts import render, redirect
from classes.models import Membership
from classes.models import Class
# =======
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

# >>>>>>> eb4da219e44bac77e16805c712580c56e806497d
from classes.models import Class, Membership
from student.models import Student


# <<<<<<< HEAD

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
# =======
def student_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.role != 'student':
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)

    return wrapped


def _student_profile(user):
    return Student.objects.select_related('user').filter(user=user).first()


@student_required
def student_dashboard(request):
    student = _student_profile(request.user)
    enrollments = Membership.objects.filter(student=student).select_related('class_obj__teacher__user') if student else Membership.objects.none()
    joined_classes = enrollments.count()
    teacher_count = enrollments.values('class_obj__teacher').distinct().count()

    return render(request, 'student/dashboard.html', {
        'joined_classes': joined_classes,
        'teacher_count': teacher_count,
        'enrollments': enrollments[:6],
    })


@student_required
def student_my_classes(request):
    student = _student_profile(request.user)
    enrollments = Membership.objects.filter(student=student).select_related('class_obj__teacher__user') if student else Membership.objects.none()

    return render(request, 'student/my_classes.html', {
        'enrollments': enrollments,
    })


@student_required
def student_teachers(request):
    student = _student_profile(request.user)
    teacher_names = []
    if student:
        teacher_names = (
            Class.objects.filter(memberships__student=student)
            .select_related('teacher__user')
            .values_list('teacher__user__username', flat=True)
            .distinct()
        )

    return render(request, 'student/teachers.html', {
        'teacher_names': teacher_names,
    })


@student_required
def student_settings_view(request):
    student = _student_profile(request.user)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()

        if username:
            request.user.username = username
        request.user.email = email
        request.user.save(update_fields=['username', 'email'])

        if student:
            student.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('student:settings')

    return render(request, 'student/settings.html', {
        'student_profile': student,
    })


@student_required
def student_profile(request):
    student = _student_profile(request.user)
    enrollments = Membership.objects.filter(student=student).select_related('class_obj') if student else Membership.objects.none()

    return render(request, 'student/profile.html', {
        'student_profile': student,
        'enrollment_count': enrollments.count(),
    })


@student_required
def student_all_classes(request):
    classes = Class.objects.select_related('teacher__user').prefetch_related('students').all()
    student = _student_profile(request.user)
    joined_classes = set()
    if student:
        joined_classes = set(
            Membership.objects.filter(student=student).values_list('class_obj_id', flat=True)
        )

    return render(request, 'student/all_classes.html', {
        'all_classes': classes,
        'joined_classes': joined_classes,
    })


@student_required
def student_join_class(request, class_id):
    if request.method != 'POST':
        return redirect('student:all_classes')

    student = get_object_or_404(Student, user=request.user)
    class_obj = get_object_or_404(Class, id=class_id)

    membership, created = Membership.objects.get_or_create(
        student=student,
        class_obj=class_obj,
    )

    if created:
        messages.success(request, f'Joined {class_obj.name}.')
    else:
        messages.info(request, f'You are already enrolled in {class_obj.name}.')

    return redirect('student:class', class_id=class_obj.id)


@student_required
def student_class(request, class_id):
    class_obj = get_object_or_404(Class.objects.select_related('teacher__user'), id=class_id)
    student = _student_profile(request.user)
    is_joined = False
    if student:
        is_joined = Membership.objects.filter(student=student, class_obj=class_obj).exists()

    return render(request, 'student/join_class.html', {
        'class_obj': class_obj,
        'is_joined': is_joined,
    })
# >>>>>>> eb4da219e44bac77e16805c712580c56e806497d
