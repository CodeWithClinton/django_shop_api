from django.urls import path , include
from .import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("cartitems", views.CartItemModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
     path("", views.product_list)
]
