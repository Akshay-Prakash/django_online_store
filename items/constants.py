from django.db import models

class ItemCategories(models.TextChoices):
    electronics = 'electronics'
    fashion = 'fashion'
    home_appliances = 'home_appliances'
    furniture = 'furniture'
    grocery = 'grocery'
    