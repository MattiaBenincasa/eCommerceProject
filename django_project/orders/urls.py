from django.urls import path
from .views import (
   checkout,
   ProcessOrderView,
   OrderConfirmation,
   MyOrders,
   CheckoutAddressSelectionView,
   CheckoutAddressCreationView
)

urlpatterns = [
   path("", checkout, name="checkout"),
   path("processOrder/", ProcessOrderView.as_view(), name="process_order"),
   path("OrderConfirmation/<int:order_id>", OrderConfirmation.as_view(), name="order_confirmation"),
   path("myOrders/", MyOrders.as_view(), name="my_orders"),
   path("select_address/", CheckoutAddressSelectionView.as_view(), name="address_selection"),
   path("add_address/", CheckoutAddressCreationView.as_view(), name="address_creation_checkout")
]
