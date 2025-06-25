from django.urls import path
from .views import MyOrders, OrderDetails


urlpatterns = [
   path("", MyOrders.as_view(), name="my_orders"),
   path("order_details/<int:order_id>", OrderDetails.as_view(), name="order_details")
]
