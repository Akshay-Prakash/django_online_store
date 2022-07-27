from rest_framework.exceptions import ValidationError


def validate_max_quantity_for_order(order_item):
    if order_item.quantity > order_item.item.stock_quantity:
        raise ValidationError(
            detail=f'{order_item.item.title} does not have {order_item.quantity} units in stock'
        )
    return True
