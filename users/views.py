from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from users.models import User, Address
from users.serializers import UserSerializer, AddressSerializer
from users.permissions import AdminOnly


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'post', 'delete']
    serializer_class = UserSerializer
    
    def get_queryset(self):
        self.queryset = User.objects.filter(id=self.request.user.id)
        return super().get_queryset()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class AddressViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = AddressSerializer

    def get_queryset(self):
        self.queryset = Address.objects.filter(user=self.request.user)
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        object.is_active = False
        object.save()
        return Response(
            data=self.get_serializer_class()(object).data,
            status=status.HTTP_200_OK
        )


class AdminUserViewSet(ModelViewSet):
    permission_classes = [AdminOnly]
    http_method_names = ['get', 'put']
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods=['put'], detail=True, permission_classes=[AdminOnly],
        serializer_class=UserSerializer)
    def make_staff(self, request, pk=None):
        user = get_object_or_404(self.get_queryset(), id=pk)
        staff_group = Group.objects.get(name='Staff')
        user.groups.add(staff_group)
        user.save()
        return Response(data={})

    @action(methods=['put'], detail=True, permission_classes=[AdminOnly],
        serializer_class=UserSerializer)
    def make_admin(self, request, pk=None):
        user = get_object_or_404(self.get_queryset(), id=pk)
        admin_group = Group.objects.get(name='Admin')
        user.groups.add(admin_group)
        user.save()
        return Response(data={})
