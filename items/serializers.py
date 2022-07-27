from rest_framework import serializers

from items.models import Item, Image


class ItemSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"

    def get_images(self, instance):
        images = Image.objects.filter(item=instance)
        return ImageSerializer(images, many=True).data


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class AddItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = (
            "id", "title", "description", "sell_price", "purchase_price",
            "universal_product_code", "category","is_active"
        )
