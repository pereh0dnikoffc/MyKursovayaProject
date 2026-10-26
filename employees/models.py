from django.db import models
from organization.models import Department, Position


class Employee(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Работает'
        FIRED = 'fired', 'Уволен'

    full_name = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees')

    # Самоссылающийся ключ (руководитель сотрудника)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')

    hire_date = models.DateField()
    fire_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return self.full_name


class EmployeePosition(models.Model):
    """Промежуточная таблица для M:N связи сотрудников и должностей"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='position_history')
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_primary = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Назначение на должность"
        verbose_name_plural = "История назначений"

    def __str__(self):
        return f"{self.employee.full_name} - {self.position.title}"