from .models import Class
from django.shortcuts import render , get_object_or_404

def class_detail(request , pk):
    class_obj = get_object_or_404(Class, pk=pk)
    

    students = class_obj.students.all()
    teacher = class_obj.teacher

    context = {
        'class_obj':class_obj,
        'students':students,
        'teacher':teacher

    }


    return render(request, 'class/class_detail.html', context )