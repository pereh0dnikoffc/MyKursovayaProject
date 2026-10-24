from django.contrib import admin
from .models import Department, Position, Grade

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'parent')
    search_fields = ('name',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'grade', 'is_manager')
    list_filter = ('department', 'is_manager')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('level', 'name', 'salary_min', 'salary_max')