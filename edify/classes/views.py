from django.shortcuts import render, redirect, get_object_or_404
from teacher.models import Teacher
from student.models import Student
from .models import Class
from .forms import ClassForm
from django.db.models import Count


def teacher_classes(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher:
        return redirect('accounts:login')

    # handle form
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.teacher = teacher   
            new_class.save()
            return redirect('classes:teacher_classes')
    else:
        form = ClassForm()

    classes = Class.objects.filter(teacher=teacher)

    context = {
        'classes': classes,
        'class_count': classes.count(),
        'form': form
    }

    return render(request, 'classes/teacher_classes.html', context)



def class_detail(request, pk):
    class_obj = Class.objects.prefetch_related('students__user').get(pk=pk)

    classes = Class.objects.filter(teacher=request.user.teacher).annotate(
        student_count=Count('students')
    )

    total_students = sum(c.student_count for c in classes)

    context = {
        'class': class_obj,          # 👉 use this in template
        'total_students': total_students
    }

    return render(request, 'classes/teacher_class_detail.html', context)
def remove_student(request, class_id, student_id):
    cls = get_object_or_404(Class, id=class_id)
    student = get_object_or_404(Student, id=student_id)

    from .models import Membership
    Membership.objects.filter(
        student=student,
        class_obj=cls
    ).delete()

    return redirect('classes:class_detail', pk=class_id)