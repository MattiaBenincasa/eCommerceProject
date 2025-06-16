from django.urls import path
from .views import (cart_detail,
                    add_to_cart,
                    remove_from_cart,
                    increment_item_quantity,
                    decrement_item_quantity)


urlpatterns = [
    path("", cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/increment/<int:item_id>", increment_item_quantity, name="increment_item_quantity"),
    path("cart/decrement/<int:item_id>", decrement_item_quantity, name="decrement_item_quantity")

]
