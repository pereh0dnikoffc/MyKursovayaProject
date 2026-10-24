from django.shortcuts import render
from .models import Vacation, Attendance

def vacation_list(request):
    vacations = Vacation.objects.all().select_related('employee')
    return render(request, 'attendance/vacation_list.html', {'vacations': vacations})

def attendance_list(request):
    records = Attendance.objects.all().select_related('employee').order_by('-work_date')[:50] # последние 50
    return render(request, 'attendance/attendance_list.html', {'records': records})