import uuid

from django.db import models
from items.constants import ItemCategories
from django.core.validators import RegexValidator

from items.validators import validate_purchase_price_lte_sell_price


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    sell_price = models.PositiveBigIntegerField()
    purchase_price = models.PositiveBigIntegerField()
    ## The UPC mentioned in bar code
    universal_product_code = models.CharField(
        max_length=15, unique=True, validators=[
            RegexValidator(
                regex='^[0-9]{12}([0-9]{2})?$',
                message='Improper Universal Product Code provided',
                code='invalid_universal_product_code'
            ),
        ]
    )
    stock_quantity = models.PositiveBigIntegerField(default=0)
    category = models.CharField(max_length=20, choices=ItemCategories.choices)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}({self.universal_product_code})'

    def clean(self):
        validate_purchase_price_lte_sell_price(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Item, self).save(*args, **kwargs)

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    image_url = models.TextField()
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='images')

    def __str__(self) -> str:
        return f'{self.item} -> {self.name}'
