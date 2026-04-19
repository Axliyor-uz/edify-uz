from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('courses/', views.student_courses, name='courses'),
    path('teachers/', views.student_teachers, name='teachers'),
    path('settings/', views.student_settings_view, name='settings'),
    path('profile/', views.student_profile, name='profile'),
]