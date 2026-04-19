from django.db import models
from teacher.models import Teacher
from student.models import Student


class Class(models.Model):
    name = models.CharField(max_length=100)

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    students = models.ManyToManyField(
        Student,
        through='Membership',
        blank=True
    )

    def __str__(self):
        return self.name
        
class Membership(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='memberships')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='memberships')
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'class_obj'],
                name='unique_student_class'
            )
        ]