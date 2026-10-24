from django.db import models


class Grade(models.Model):
    name = models.CharField(max_length=50)
    level = models.PositiveSmallIntegerField(unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.level}. {self.name}"


class Department(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True, null=True)

    # Самоссылающийся ключ (иерархия отделов)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    # Руководитель отдела. Ссылается на модель Employee (из другого приложения)
    # Используем строку 'employees.Employee', чтобы избежать циклического импорта
    head = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='headed_departments')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions')
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, related_name='positions')
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.department.name})"