from django.urls import path
from .views import (
   MyOrders,
   OrderDetails,
   CustomersOrders,
   ChangeOrderStatus
)


urlpatterns = [
   path("", MyOrders.as_view(), name="my_orders"),
   path("order_details/<int:order_id>", OrderDetails.as_view(), name="order_details"),
   path("customers_orders/", CustomersOrders.as_view(), name="customers_orders"),
   path("change_order_status/<int:pk>", ChangeOrderStatus.as_view(), name="change_order_status")
]
