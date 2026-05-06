from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.views.decorators.http import require_POST

from teacher.models import Teacher
from student.models import Student

from .models import Class, Assignment, Submission, AssignmentFile, Membership
from .forms import ClassForm

#  DECORATORS

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.role != 'teacher':
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.role != 'student':
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper





# TEACHER -CLASSES

@teacher_required
def teacher_classes(request):
    teacher = request.user.teacher

    if request.method == "POST":
        form = ClassForm(request.POST)
        if form.is_valid():
            cls = form.save(commit=False)
            cls.teacher = teacher
            cls.save()
            return redirect("classes:teacher_classes")
    else:
        form = ClassForm()

    classes = Class.objects.filter(teacher=teacher)

    return render(request, "classes/teacher_classes.html", {
        "classes": classes,
        "class_count": classes.count(),
        "form": form
    })



@teacher_required
def teacher_class_detail(request, id):
    teacher = request.user.teacher

    cls = get_object_or_404(Class, id=id, teacher=teacher)

    assignments = Assignment.objects.filter(
        teacher=teacher,
        classes=cls
    ).distinct()

    return render(request, "classes/teacher_class_detail.html", {
        "class": cls,
        "assignments": assignments
    })



@teacher_required
def remove_student(request, class_id, student_id):
    cls = get_object_or_404(Class, id=class_id)
    student = get_object_or_404(Student, id=student_id)

    Membership.objects.filter(
        class_obj=cls,
        student=student
    ).delete()

    return redirect("classes:class_detail", pk=class_id)









# ASSIGNMENTS

@teacher_required
def create_assignment(request):
    teacher = request.user.teacher

    if request.method == "POST":
        assignment = Assignment.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            teacher=teacher
        )

        class_ids = request.POST.getlist("classes")
        assignment.classes.set(Class.objects.filter(id__in=class_ids))

        for f in request.FILES.getlist("files"):
            AssignmentFile.objects.create(
                assignment=assignment,
                file=f
            )

        return redirect("classes:assignments")

    return render(request, "classes/teacher_create_assignment.html", {
        "classes": Class.objects.filter(teacher=teacher)
    })



@teacher_required
def teacher_assignments(request):
    teacher = request.user.teacher

    assignments = Assignment.objects.filter(
        teacher=teacher
    ).prefetch_related("classes")

    return render(request, "classes/teacher_assignment_page.html", {
        "assignments": assignments
    })


def assignment_detail(request, id):
    assignment = get_object_or_404(Assignment, id=id)

    # TEACHER VIEW
    if request.user.is_authenticated and request.user.role == "teacher":
        submissions = Submission.objects.filter(assignment=assignment)
        return render(request, "classes/teacher_assignment_detail.html", {
            "assignment": assignment,
            "submissions": submissions,
        })

    #  STUDENT VIEW
    if request.user.is_authenticated and request.user.role == "student":
        submission = Submission.objects.filter(
            assignment=assignment,
            student=request.user.student
        ).first()

        return render(request, "classes/student_assignment_detail.html", {
            "assignment": assignment,
            "submission": submission,
        })

    return redirect("accounts:login")



@teacher_required
def delete_assignment(request, id):
    teacher = request.user.teacher
    assignment = get_object_or_404(Assignment, id=id, teacher=teacher)

    if request.method == "POST":
        assignment.delete()
        return redirect("classes:assignments")

    return render(request, "teacher/confirm_delete.html", {
        "assignment": assignment
    })


@teacher_required
def remove_class_from_assignment(request, assignment_id, class_id):
    teacher = request.user.teacher

    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=teacher)
    cls = get_object_or_404(Class, id=class_id, teacher=teacher)

    if request.method == "POST":
        assignment.classes.remove(cls)

    return redirect("classes:assignment_detail", id=assignment.id)







# STUDENT -CLASS
@student_required
def student_class_detail(request, id):
    cls = get_object_or_404(Class, id=id)
    student = request.user.student

    assignments = Assignment.objects.filter(
        classes=cls
    ).select_related("teacher__user").prefetch_related("files")

    submissions = Submission.objects.filter(
        student=student,
        assignment__in=assignments
    )

    submitted_ids = set(submissions.values_list("assignment_id", flat=True))

    return render(request, "classes/student_classes_detail.html", {
        "class": cls,
        "assignments": assignments,
        "submitted_ids": submitted_ids,
    })


@student_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student

    if request.method == "POST":
        file = request.FILES.get("file")

        if file:
            Submission.objects.update_or_create(
                student=student,
                assignment=assignment,
                defaults={"file": file}
            )

    cls = assignment.classes.filter(students=student).first()

    if cls:
        return redirect("classes:student_class_detail", id=cls.id)

    return redirect("classes:student_dashboard")







# CLASS DETAIL

def class_detail(request, pk):
    cls = get_object_or_404(Class.objects.prefetch_related("students__user"), pk=pk)

    classes = Class.objects.filter(teacher=cls.teacher).annotate(
        student_count=Count("students")
    )

    total_students = sum(c.student_count for c in classes)

    return render(request, "classes/teacher_class_detail.html", {
        "class": cls,
        "total_students": total_students
    })







# GRADING

@require_POST
def grade_submission(request, submission_id):
    if not request.user.is_authenticated or request.user.role != "teacher":
        return redirect("accounts:login")

    submission = get_object_or_404(
        Submission.objects.select_related("assignment__teacher"),
        id=submission_id
    )

    if submission.assignment.teacher != request.user.teacher:
        return redirect("classes:assignments")

    raw_grade = request.POST.get("grade", "").strip()

    if raw_grade == "":
        submission.grade = None
    else:
        try:
            grade = int(raw_grade)
            if 0 <= grade <= 100:
                submission.grade = grade
        except ValueError:
            pass

    submission.save(update_fields=["grade"])

    return redirect("classes:assignment_detail", id=submission.assignment_id)