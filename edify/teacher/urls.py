from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='dashboard'),
    path('courses/', views.teacher_courses, name='courses'),
    path('students/', views.teacher_students, name='students'),
    path('settings/', views.teacher_settings_view, name='settings'),
    path('profile/', views.teacher_profile, name='profile'),
    # path('classes/', views.teacher_classes, name='classes'),
    
]