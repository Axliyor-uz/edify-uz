from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('teacher/', views.teacher_classes, name='teacher_classes'),
]