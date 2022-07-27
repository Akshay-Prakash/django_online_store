from django.contrib import admin

from orders.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_time', 'user', 'total_price',
                    'total_quantity', 'total_items')
    readonly_fields = (
        'id', 'order_time', 'user', 'total_price', 'total_quantity',
        'total_items', 'billing_address', 'shipping_address'
    )


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'rate', 'value')
    readonly_fields = ('order', 'item', 'quantity', 'rate', 'value')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
