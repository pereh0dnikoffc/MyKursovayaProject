from django import forms
from .models import Department, Position, Grade


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'parent', 'head']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'head': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')

        # Проверка: отдел не может быть родителем сам себе
        if self.instance and parent and self.instance.pk == parent.pk:
            raise forms.ValidationError("Отдел не может быть родительским по отношению к самому себе.")
        return cleaned_data


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'department', 'grade', 'is_manager']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'is_manager': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }