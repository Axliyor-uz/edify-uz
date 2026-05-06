from collections import defaultdict

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from classes.models import Class, Membership
from student.models import Student


def student_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'student':
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)

    return wrapped



def get_student(user):
    return Student.objects.select_related('user').filter(user=user).first()


@student_required
def student_dashboard(request):
    student = get_student(request.user)
    enrollments = Membership.objects.filter(student=student).select_related('class_obj__teacher__user') if student else Membership.objects.none()

    return render(request, 'student/dashboard.html', {
        'joined_classes': enrollments.count(),
        'teacher_count': enrollments.values('class_obj__teacher').distinct().count(),
        'enrollments': enrollments[:6],
    })


@student_required
def student_my_classes(request):
    student = get_student(request.user)
    enrollments = Membership.objects.filter(student=student).select_related('class_obj__teacher__user') if student else Membership.objects.none()

    return render(request, 'student/my_classes.html', {
        'enrollments': enrollments,
    })


@student_required
def student_teachers(request):
    student = get_student(request.user)
    teacher_map = defaultdict(list)

    if student:
        memberships = Membership.objects.filter(student=student).select_related('class_obj__teacher__user')
        for membership in memberships:
            teacher_map[membership.class_obj.teacher].append(membership.class_obj)

    teacher_cards = [
        {
            'teacher': teacher,
            'classes': classes,
            'class_count': len(classes),
        }
        for teacher, classes in teacher_map.items()
    ]

    return render(request, 'student/teachers.html', {
        'teacher_cards': teacher_cards,
    })


@student_required
def student_settings_view(request):
    student = get_student(request.user)

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
    student = get_student(request.user)
    enrollments = Membership.objects.filter(student=student).select_related('class_obj__teacher__user') if student else Membership.objects.none()

    return render(request, 'student/profile.html', {
        'enrollments': enrollments,
        'enrollment_count': enrollments.count(),
    })


@student_required
def student_all_classes(request):
    student = get_student(request.user)
    joined_classes = []

    if student:
        joined_classes = list(
            Membership.objects.filter(student=student).values_list('class_obj_id', flat=True)
        )

    classes = Class.objects.select_related('teacher__user').all()
    return render(request, 'student/all_classes.html', {
        'all_classes': classes,
        'joined_classes': joined_classes,
    })


@student_required
def student_join_class(request, class_id):
    student = get_student(request.user)
    class_obj = get_object_or_404(Class, id=class_id)

    Membership.objects.get_or_create(student=student, class_obj=class_obj)
    return redirect('student:class', class_id=class_obj.id)


@student_required
def student_class(request, class_id):
    student = get_student(request.user)
    class_obj = get_object_or_404(Class.objects.select_related('teacher__user'), id=class_id)
    is_joined = False

    if student:
        is_joined = Membership.objects.filter(student=student, class_obj=class_obj).exists()

    return render(request, 'student/join_class.html', {
        'class_obj': class_obj,
        'is_joined': is_joined,
    })
