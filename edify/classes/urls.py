from django.urls import path
from . import views
from .views import class_detail

app_name = 'classes'

urlpatterns = [
    path('teacher/', views.teacher_classes, name='teacher_classes'),
    path('<int:pk>/', views.class_detail, name='class_detail'),
]