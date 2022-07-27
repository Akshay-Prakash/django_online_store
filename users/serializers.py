from xml.etree.ElementInclude import include
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from users.models import User, Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'last_name', 'first_name', 'email',
            'mobile_number', 'addresses', 'password'
        )

    def create(self, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(
                validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(
                validated_data["password"])
        return super().update(instance, validated_data)

    def get_addresses(self, instance):
        addresses = Address.objects.filter(user=instance)
        return AddressSerializer(addresses, many=True).data
