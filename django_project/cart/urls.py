from django.urls import path
from .views import cart_detail, add_to_cart


urlpatterns = [
    path("", cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
]
