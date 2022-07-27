from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from items.models import Item, Image
from items.serializers import ItemSerializer, ImageSerializer, AddItemSerializer
from users.permissions import AdminOnly, StaffOnly


class ItemViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['get']
    serializer_class = ItemSerializer
    queryset = Item.objects.filter(is_active=True)


class AdminItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, AdminOnly]
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        object.is_active = False
        object.save()
        return Response(
            data=self.get_serializer_class()(object).data,
            status=status.HTTP_200_OK
        )

    @action(methods=['put'], detail=True, 
        permission_classes=[IsAuthenticated, AdminOnly or StaffOnly],
        serializer_class=AddItemSerializer)
    def add_stock(self, request, pk=None):
        item = get_object_or_404(self.get_queryset(), id=pk)
        item.stock_quantity += request.data["stock_quantity"]
        item.save()
        return Response(
            data=self.get_serializer_class()(item).data,
            status=status.HTTP_200_OK
        )


class AdminImageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, AdminOnly]
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
