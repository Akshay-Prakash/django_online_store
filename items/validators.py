from rest_framework.exceptions import ValidationError

def validate_purchase_price_lte_sell_price(item):
    if item.purchase_price > item.sell_price:
        raise ValidationError(
            detail=f'Sell price: {item.sell_price} is less than purchase price: {item.purchase_price} for product {item.title}({item.universal_product_code}).'
        )
    return True
