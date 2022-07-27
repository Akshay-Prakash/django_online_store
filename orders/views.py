from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import OrderSerializer, OrderItemSerializer
from users.permissions import AdminOnly, StaffOnly


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    serializer_class = OrderSerializer

    def get_queryset(self):
        self.queryset = Order.objects.all(user=self.request.user)
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        order_items = request.data.pop("order_items", {})
        
        context = {
                    "request": self.request,
                }
        order_serializer = OrderSerializer(data=request.data, context=context)
        if order_serializer.is_valid(raise_exception=True):
            order = order_serializer.save()
        
        order_items_serializer = []
        for order_item in order_items:
            order_item["order"] = str(order.id)
            order_item_serializer = OrderItemSerializer(data=order_item)
            if order_item_serializer.is_valid(raise_exception=True):
                order_items = order_item_serializer.save()
                order_items_serializer.append(dict(order_item_serializer.data))

        order = Order.objects.get(id = order_serializer.data["id"])
        order_serializer = OrderSerializer(order, context=context)
        order_serializer_data = dict(order_serializer.data)
        order_serializer_data["order_items"] = order_items_serializer

        headers = self.get_success_headers(order_serializer.data)
        return Response(
            order_serializer_data, status=status.HTTP_201_CREATED,
            headers=headers
        )


class AdminOrderViewSet(ModelViewSet):
    permission_classes = [AdminOnly or StaffOnly]
    http_method_names = ['get']
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
