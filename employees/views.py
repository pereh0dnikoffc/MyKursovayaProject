from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Prefetch
from .models import Employee, EmployeePosition
from .forms import HireEmployeeForm
from .services import hire_employee


def employee_list(request):
    # Заранее подгружаем текущие должности (где end_date пустая), чтобы не делать
    # запрос в БД для каждой строки таблицы
    current_positions = EmployeePosition.objects.filter(end_date__isnull=True).select_related('position')

    employees = Employee.objects.all().select_related('department').prefetch_related(
        Prefetch('position_history', queryset=current_positions, to_attr='current_positions')
    )

    return render(request, 'employees/list.html', {'employees': employees})

def hire_employee_view(request):
    if request.method == 'POST':
        form = HireEmployeeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            hire_employee(
                full_name=cd['full_name'],
                department=cd['department'],
                position=cd['position'],
                hire_date=cd['hire_date'],
                manager=cd['manager']
            )
            messages.success(request, "Сотрудник успешно нанят!")
            return redirect('employee_list')
    else:
        form = HireEmployeeForm()

    return render(request, 'employees/hire_form.html', {'form': form})

def dashboard(request):
    # Простая страница-заглушка
    return render(request, 'dashboard.html')