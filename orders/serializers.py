from rest_framework import serializers

from orders.models import Order, OrderItem
from users.models import User


class OrderItemSerializer(serializers.ModelSerializer):
    # order = serializers.CharField(required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(
        many=True, required=False, source='items'
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Order
        fields = "__all__"
        read_only = ('order_items',)

    def get_order_items(self, instance):
        order_items = instance.get_order_items
        return OrderItemSerializer(order_items, many=True).data
