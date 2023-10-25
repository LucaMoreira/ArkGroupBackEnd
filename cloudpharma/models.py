from django.db import models
from beta.models import User
from .utils import get_dates_delta, calculate_daily
from django.db.models.signals import post_save
from django.dispatch import receiver

CONSUMPTION_CHOICES = (
    ("1", "Domingo"),
    ("2", "Segunda"),
    ("3", "Terca"),
    ("4", "Quarta"),
    ("5", "Quinta"),
    ("6", "Sexta"),
    ("7", "Sabado")
)

class Choice(models.Model):
    choice = models.CharField(max_length=50, choices=CONSUMPTION_CHOICES, unique=True)
    
    def __str__(self):
        return CONSUMPTION_CHOICES[int(self.choice) - 1][1]

class Medcine(models.Model):
    id              = models.AutoField(primary_key=True)
    name            = models.CharField(max_length=50)
    consumption     = models.ManyToManyField(Choice)
    amount_consumed = models.SmallIntegerField()
    initial_amount  = models.SmallIntegerField()
    actual_amount   = models.SmallIntegerField(null=True)
    purchase_date   = models.DateField()
    end_date        = models.DateField(null=True)
    owner           = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + f' ({self.owner} | {self.purchase_date})'


@receiver(post_save, sender=Medcine, dispatch_uid="update_medcine")
def update_medcine(sender, instance, **kwargs):
    dates                                     = get_dates_delta(str(instance.purchase_date))
    instance.actual_amount, instance.end_date = calculate_daily(dates, instance.consumption, instance.initial_amount, instance.amount_consumed)
