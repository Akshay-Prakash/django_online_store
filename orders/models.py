import uuid

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

from users.models import Address
from items.models import Item
from orders.validators import validate_max_quantity_for_order
from users.validators import validate_address_belongs_to_user

User = get_user_model()


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders")
    order_time = models.DateTimeField(auto_now_add=True, editable=False)
    total_price = models.PositiveBigIntegerField(editable=False)
    total_quantity = models.PositiveIntegerField(editable=False)
    total_items = models.PositiveIntegerField(editable=False)
    billing_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="orders_billed")
    shipping_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="orders_shipped")

    def __str__(self) -> str:
        return f'{self.user} -> {self.order_time}'

    def get_order_items(self):
        return self.items.all()

    def clean(self):
        validate_address_belongs_to_user(self.user, self.billing_address)
        validate_address_belongs_to_user(self.user, self.shipping_address)

    def save(self, *args, **kwargs):
        self.full_clean()
        self.total_items = self.total_items or 0
        self.total_quantity = self.total_quantity or 0
        self.total_price = self.total_price or 0
        return super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])
    rate = models.PositiveIntegerField(editable=False)
    value = models.PositiveIntegerField(editable=False)

    def __str__(self) -> str:
        return f'{self.order.user} -> {self.order.order_time} -> {self.item}'

    def clean(self):
        validate_max_quantity_for_order(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        # update self attributes
        self.rate = self.item.sell_price
        self.value = self.rate * self.quantity

        # update order attributes
        self.order.total_items += 1
        self.order.total_quantity += self.quantity
        self.order.total_price += self.value
        self.order.save()

        # update item stock
        self.item.stock_quantity -= self.quantity
        self.item.save()

        return super(OrderItem, self).save(*args, **kwargs)
