from django.shortcuts import render, redirect
from teacher.models import Teacher
from .models import Class
from .forms import ClassForm

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