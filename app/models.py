from __future__ import unicode_literals

from cpf_field.models import CPFField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
# Create your models here.
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from phone_field import PhoneField


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now=True)


class Category(TimeStamped):
    name = models.CharField(max_length=225, blank=True, null=True)
    stock = models.PositiveIntegerField()
    address = models.CharField(max_length=225, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name
