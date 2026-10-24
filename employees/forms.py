from django import forms
from .models import Employee
from organization.models import Department, Position

class HireEmployeeForm(forms.Form):
    """
    Кастомная форма (не ModelForm), так как мы будем передавать данные
    в нашу сервисную функцию hire_employee().
    """
    full_name = forms.CharField(
        max_length=150,
        label="ФИО",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="Отдел",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        label="Должность",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    hire_date = forms.DateField(
        label="Дата приема",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    manager = forms.ModelChoiceField(
        queryset=Employee.objects.filter(status=Employee.Status.ACTIVE),
        required=False,
        label="Руководитель",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class EmployeeUpdateForm(forms.ModelForm):
    """
    Обычная ModelForm для редактирования существующих данных.
    """
    class Meta:
        model = Employee
        fields = ['full_name', 'department', 'manager', 'status', 'fire_date']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'fire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }