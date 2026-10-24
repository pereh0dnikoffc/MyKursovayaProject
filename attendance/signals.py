from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Vacation

@receiver(pre_save, sender=Vacation)
def check_vacation_dates(sender, instance, **kwargs):

    if instance.end_date < instance.start_date:
        from django.core.exceptions import ValidationError
        raise ValidationError("Дата окончания отпуска не может быть раньше даты начала.")