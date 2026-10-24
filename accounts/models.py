from django.db import models
from employees.models import Employee


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class User(models.Model):
    # Связь 1:1. У одного сотрудника может быть только один аккаунт.
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='account')
    login = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Связь M:N. Django автоматически создаст таблицу связей (roles_users)
    roles = models.ManyToManyField(Role, related_name='users')

    def __str__(self):
        return self.login