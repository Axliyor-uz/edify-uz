from django.urls import path
from . import forms

app_name = 'student'

urlpatterns = [
    path('dashboard/', forms.student_dashboard, name='dashboard'),
    path('myclasses/', forms.student_my_classes, name='my_classes'),
    path('teachers/', forms.student_teachers, name='teachers'),
    path('settings/', forms.student_settings_view, name='settings'),
    path('profile/', forms.student_profile, name='profile'),
    path('allclasses/', forms.student_all_classes, name='all_classes'),
    path('join_class/<int:class_id>/', forms.student_join_class, name='join_class'),
    path('class/<int:class_id>/', forms.student_class, name='class'),
]