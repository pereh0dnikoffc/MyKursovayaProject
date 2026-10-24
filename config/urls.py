from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Подключаем маршруты нашего приложения employees
    path('', include('employees.urls')), 
]