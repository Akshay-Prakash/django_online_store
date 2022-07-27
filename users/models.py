import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mobile_number = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]*$',
            message='Improper mobile number provided',
            code='invalid_mobile_number'
        ),
    ])

    def __str__(self):
        return f'{self.username}'


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    latitude = models.CharField(max_length=10, null=True, blank=True)
    longitude = models.CharField(max_length=10, null=True, blank=True)
    gcode = models.CharField(max_length=10, null=True, blank=True)
    line1 = models.CharField(max_length=100, null=True, blank=True)
    line2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="addresses"
    )

    def __str__(self):
        return f'{self.user} -> {self.name}'

    class Meta:
        unique_together = [['name', 'user']]
