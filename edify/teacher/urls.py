from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='dashboard'),
    path('assignments/', views.teacher_assignments, name='assignments'),
    path('students/', views.teacher_students, name='students'),
    path('settings/', views.teacher_settings_view, name='settings'),
    path('profile/', views.teacher_profile, name='profile'),
    path('classes/', views.teacher_create_class, name='create_class'),
    path('allclasses/', views.teacher_classes, name='allclasses'),
    # path('classes/', views.teacher_classes, name='classes'),
    path('settings/', views.teacher_settings, name='settings'),
    # path('delete/', views.delete_account, name='delete_account'),
    # path("assignments/create/", views.create_assignment, name="create_assignment")
    
]