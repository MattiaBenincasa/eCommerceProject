from django.urls import path
from .views import checkout, process_order,OrderConfirmation

urlpatterns = [
   path("", checkout, name="checkout"),
   path("processOrder/", process_order, name="process_order"),
   path("OrderConfirmation/<int:order_id>", OrderConfirmation.as_view(), name="order_confirmation")
]
