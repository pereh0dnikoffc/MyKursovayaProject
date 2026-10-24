from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee
from .forms import HireEmployeeForm
from .services import hire_employee

def employee_list(request):
    employees = Employee.objects.all().select_related('department')
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