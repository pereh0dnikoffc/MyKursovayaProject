from django.contrib import admin
from .models import Vacation, SickLeave, Attendance, VacationBalance

@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'days_count', 'status')
    list_filter = ('status', 'vacation_type')

@admin.register(SickLeave)
class SickLeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'status')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('work_date', 'employee', 'day_type', 'hours_worked')
    list_filter = ('day_type', 'work_date')

@admin.register(VacationBalance)
class VacationBalanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'year', 'total_days', 'used_days', 'remaining_days')
    list_filter = ('year',)