from django.urls import path, include
from orders import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("orders", views.OrderViewSet, basename='Order')
router.register("admin/orders", views.AdminOrderViewSet, basename='AdminOrder')

urlpatterns = [
    path('', include(router.urls)),
]
