from django.db import transaction
from django.utils import timezone
from .models import Employee, EmployeePosition
from attendance.models import VacationBalance


@transaction.atomic  # Если произойдет ошибка, БД откатит все изменения
def hire_employee(full_name, department, position, hire_date, manager=None, salary_grade=None):

    # 1. Создаем карточку сотрудника
    employee = Employee.objects.create(
        full_name=full_name,
        department=department,
        hire_date=hire_date,
        manager=manager,
        status=Employee.Status.ACTIVE
    )

    # 2. Назначаем на должность
    EmployeePosition.objects.create(
        employee=employee,
        position=position,
        start_date=hire_date,
        is_primary=True
    )

    # 3. Создаем баланс отпускных на текущий год (например, 28 дней)
    VacationBalance.objects.create(
        employee=employee,
        year=hire_date.year,
        total_days=28,
        used_days=0,
        remaining_days=28
    )

    return employee


@transaction.atomic
def fire_employee(employee_id, fire_date=None):

    if not fire_date:
        fire_date = timezone.now().date()

    employee = Employee.objects.get(id=employee_id)
    employee.status = Employee.Status.FIRED
    employee.fire_date = fire_date
    employee.save()

    # Закрываем текущую должность (проставляем дату окончания)
    current_position = EmployeePosition.objects.filter(employee=employee, end_date__isnull=True).first()
    if current_position:
        current_position.end_date = fire_date
        current_position.save()

    return employee