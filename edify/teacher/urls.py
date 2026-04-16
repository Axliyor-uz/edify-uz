from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name = 'dashboard')
]