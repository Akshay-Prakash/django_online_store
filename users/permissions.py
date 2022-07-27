from rest_framework import permissions
from django.contrib.auth.models import Group


class AdminOnly(permissions.BasePermission):
    # admin_group = Group.objects.get(name='Admin')

    def has_permission(self, request, view):
        admin_group = Group.objects.get(name='Admin')
        return admin_group in request.user.groups.all()

    def has_object_permission(self, request, view, obj):
        admin_group = Group.objects.get(name='Admin')
        return admin_group in request.user.groups.all()

class StaffOnly(permissions.BasePermission):
    # staff_group = Group.objects.get(name='Staff')

    def has_permission(self, request, view):
        staff_group = Group.objects.get(name='Staff')
        return staff_group in request.user.groups.all()

    def has_object_permission(self, request, view, obj):
        staff_group = Group.objects.get(name='Staff')
        return staff_group in request.user.groups.all()
