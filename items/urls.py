from django.urls import path, include
from items import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register("items", views.ItemViewSet, basename='Item')

router.register("admin/items", views.AdminItemViewSet, basename='AdminItem')
router.register("admin/images", views.AdminImageViewSet, basename='AdminImage')

urlpatterns = [
    path('', include(router.urls)),
]
