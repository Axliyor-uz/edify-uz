from django.db import models
from django.utils import timezone
from teacher.models import Teacher
from student.models import Student


class Class(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True , help_text='class description')
    created_at = models.DateTimeField(auto_now_add=True)

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE , 
        related_name = 'classes'
    )

    students = models.ManyToManyField(
        Student,
        through='Membership',
        blank=True
    )

    def __str__(self):
        return self.name
    
    def get_student_count(self):
        return self.students.count()
    
    class Meta:
        verbose_name_plural = "Classes"
        ordering = ['-created_at']

        
class Membership(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='memberships')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='memberships')
    date_joined = models.DateField(auto_now_add = True)
    invite_reason = models.CharField(max_length=64, blank = True, default = "Self-enrolled" )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'class_obj'],
                name='unique_student_class'
            )
        ]

    def __str__(self):
        return f"{self.student.user.username} in {self.class_obj.name}"

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    teacher = models.ForeignKey('teacher.Teacher', on_delete=models.CASCADE)

    classes = models.ManyToManyField('classes.Class')

    created_at = models.DateTimeField(auto_now_add=True)