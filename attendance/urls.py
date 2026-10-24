from django.urls import path
from . import views

urlpatterns = [
    path('vacations/', views.vacation_list, name='vacation_list'),
    path('attendance/', views.attendance_list, name='attendance_list'),
]