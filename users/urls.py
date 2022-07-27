from django.urls import path, include
from users import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register("users", views.UserViewSet, basename='User')
router.register("addresses", views.AddressViewSet, basename='Address')

router.register("admin/users", views.AdminUserViewSet, basename='AdminUser')

urlpatterns = [
    path('', include(router.urls)),
]
