from django.urls import path
from .views import MyOrders


urlpatterns = [
   path("", MyOrders.as_view(), name="my_orders"),
]
