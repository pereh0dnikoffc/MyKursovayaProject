from django import forms
from .models import Vacation, SickLeave, Attendance


class VacationForm(forms.ModelForm):
    class Meta:
        model = Vacation
        # Поля, которые заполняет пользователь
        fields = ['start_date', 'end_date', 'vacation_type']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'vacation_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("Дата окончания не может быть раньше даты начала.")

            # Автоматически считаем дни и записываем в скрытое поле модели
            # (модель Vacation требует days_count)
            delta = end_date - start_date
            cleaned_data['days_count'] = delta.days + 1

        return cleaned_data

    def save(self, commit=True):
        # Переопределяем save, чтобы сохранить вычисленный days_count
        instance = super().save(commit=False)
        instance.days_count = self.cleaned_data['days_count']
        if commit:
            instance.save()
        return instance


class SickLeaveForm(forms.ModelForm):
    class Meta:
        model = SickLeave
        fields = ['start_date', 'end_date', 'document_no']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'document_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер листа'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("Дата окончания больничного не может быть раньше даты начала.")
        return cleaned_data