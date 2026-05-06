from django.urls import path
from . import views
from .views import class_detail

app_name = 'classes'

urlpatterns = [
    path('teacher/', views.teacher_classes, name='teacher_classes'),
    path('<int:pk>/', views.class_detail, name='class_detail'),
    path('<int:class_id>/remove/<int:student_id>/', views.remove_student, name='remove_student'),
    path('assignments/', views.teacher_assignments, name='assignments'),
    path("assignments/create/", views.create_assignment, name="create_assignment"),
    path("assignments/<int:id>/", views.assignment_detail, name="assignment_detail"),
    path('assignment/<int:id>/delete/', views.delete_assignment, name='delete_assignment'),
    path('assignment/<int:assignment_id>/remove-class/<int:class_id>/', views.remove_class_from_assignment, name='remove_class_from_assignment'),
    path('class/<int:id>/', views.student_class_detail, name='student_class_detail'),
    path('teacher/class/<int:id>/', views.teacher_class_detail, name='teacher_class_detail'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submission/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),

]