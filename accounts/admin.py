from django.contrib import admin
from .models import User, Role

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'employee', 'is_active', 'last_login')
    list_filter = ('is_active',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')