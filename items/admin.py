from django.contrib import admin

from items.models import Image, Item


class ImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'name', 'image_url')
    readonly_fields = ('item',)


class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'sell_price', 'purchase_price',
        'universal_product_code', 'stock_quantity', 'category',
        'is_active', 'id'
    )

admin.site.register(Image, ImageAdmin)
admin.site.register(Item, ItemAdmin)
