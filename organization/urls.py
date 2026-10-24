from django.urls import path
from . import views

urlpatterns = [
    path('departments/', views.department_list, name='department_list'),
]