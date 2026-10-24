from django.contrib import admin
from .models import Employee, EmployeePosition

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'status', 'hire_date')
    list_filter = ('status', 'department')
    search_fields = ('full_name',)

@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'position', 'start_date', 'end_date', 'is_primary')
    list_filter = ('is_primary',)