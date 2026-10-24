from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import Vacation, VacationBalance, Attendance, SickLeave


@transaction.atomic
def approve_vacation(vacation_id, approver):

    vacation = Vacation.objects.get(id=vacation_id)

    if vacation.status != Vacation.Status.PENDING:
        raise ValidationError("Можно одобрить только заявку в статусе 'На согласовании'.")

    # 1. Проверяем баланс на год начала отпуска
    balance = VacationBalance.objects.get(employee=vacation.employee, year=vacation.start_date.year)

    if balance.remaining_days < vacation.days_count:
        raise ValidationError(f"Недостаточно дней. Остаток: {balance.remaining_days}, запрошено: {vacation.days_count}")

    # 2. Списываем дни
    balance.used_days += vacation.days_count
    balance.remaining_days -= vacation.days_count
    balance.save()

    # 3. Меняем статус заявки
    vacation.status = Vacation.Status.APPROVED
    vacation.approved_by = approver
    vacation.save()

    # 4. Автоматически заполняем табель (Attendance)
    current_date = vacation.start_date
    while current_date <= vacation.end_date:
        # update_or_create позволяет перезаписать день, если там уже что-то было
        Attendance.objects.update_or_create(
            employee=vacation.employee,
            work_date=current_date,
            defaults={
                'day_type': Attendance.DayType.VACATION,
                'hours_worked': 0,
                'comment': f"Отпуск #{vacation.id}"
            }
        )
        current_date += timedelta(days=1)


@transaction.atomic
def close_sick_leave(sick_leave_id):

    sick_leave = SickLeave.objects.get(id=sick_leave_id)
    if sick_leave.status == SickLeave.Status.CLOSED:
        return

    sick_leave.status = SickLeave.Status.CLOSED
    sick_leave.save()

    # Заполняем табель днями больничного
    current_date = sick_leave.start_date
    while current_date <= sick_leave.end_date:
        Attendance.objects.update_or_create(
            employee=sick_leave.employee,
            work_date=current_date,
            defaults={
                'day_type': Attendance.DayType.SICK,
                'hours_worked': 0,
                'comment': f"Больничный #{sick_leave.id}"
            }
        )
        current_date += timedelta(days=1)