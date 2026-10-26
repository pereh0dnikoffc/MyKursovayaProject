from django.db import models
from employees.models import Employee


class VacationBalance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='vacation_balances')
    year = models.PositiveIntegerField()
    total_days = models.IntegerField(default=28)
    used_days = models.IntegerField(default=0)

    # Можно оставить как обычное поле int, но лучше сделать свойством (см. ниже)
    remaining_days = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Отпускные"
        verbose_name_plural = "Отпускные"
        unique_together = ('employee', 'year')  # У сотрудника один баланс на год

    def save(self, *args, **kwargs):
        # Автоматический расчет остатка перед сохранением
        self.remaining_days = self.total_days - self.used_days
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.full_name} - {self.year} ({self.remaining_days} дней)"


class Vacation(models.Model):
    class VacationType(models.TextChoices):
        ANNUAL = 'annual', 'Ежегодный'
        UNPAID = 'unpaid', 'Без сохранения зарплаты'
        STUDY = 'study', 'Учебный'

    class Status(models.TextChoices):
        PENDING = 'pending', 'На согласовании'
        APPROVED = 'approved', 'Одобрен'
        REJECTED = 'rejected', 'Отклонен'
        CANCELLED = 'cancelled', 'Отменен'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='vacations')
    start_date = models.DateField()
    end_date = models.DateField()
    days_count = models.IntegerField()
    vacation_type = models.CharField(max_length=20, choices=VacationType.choices, default=VacationType.ANNUAL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    # Кто одобрил (руководитель)
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='approved_vacations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отпуск"
        verbose_name_plural = "Отпуска"


class SickLeave(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Открыт'
        CLOSED = 'closed', 'Закрыт'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='sick_leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    document_no = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Больничный"
        verbose_name_plural = "Больничные"


class Attendance(models.Model):
    class DayType(models.TextChoices):
        WORK = 'work', 'Рабочий'
        WEEKEND = 'weekend', 'Выходной'
        HOLIDAY = 'holiday', 'Праздник'
        VACATION = 'vacation', 'Отпуск'
        SICK = 'sick', 'Больничный'
        ABSENT = 'absent', 'Прогул'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    work_date = models.DateField()
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    day_type = models.CharField(max_length=20, choices=DayType.choices, default=DayType.WORK)
    comment = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Посещаемость"
        verbose_name_plural = "Посещаемость"
        # Один сотрудник - одна запись в день
        unique_together = ('employee', 'work_date') 