# config/urls.py (или как называется папка проекта)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('employees.urls')),
    path('', include('organization.urls')),
    path('', include('attendance.urls')),
]