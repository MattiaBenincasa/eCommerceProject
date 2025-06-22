from django.urls import path
from .views import (
    CheckoutAddressSelectionView,
    CheckoutAddressCreationView,
    ProcessOrderView,
    OrderConfirmation
)


urlpatterns = [
    path('', CheckoutAddressSelectionView.as_view(), name="address_selection"),
    path("add_address/", CheckoutAddressCreationView.as_view(), name="address_creation_checkout"),
    path("processOrder/", ProcessOrderView.as_view(), name="process_order"),
    path("OrderConfirmation/<int:order_id>", OrderConfirmation.as_view(), name="order_confirmation"),
]
