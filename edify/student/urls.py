from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('myclasses/', views.student_my_classes, name='my_classes'),
    path('teachers/', views.student_teachers, name='teachers'),
    path('settings/', views.student_settings_view, name='settings'),
    path('profile/', views.student_profile, name='profile'),
    path('allclasses/', views.student_all_classes, name='all_classes'),
    path('join_class/<int:class_id>/', views.student_join_class, name='join_class'),
    path('class/<int:class_id>/', views.student_class, name='class'),
]