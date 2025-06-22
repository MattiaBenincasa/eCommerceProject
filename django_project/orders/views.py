from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Order


class MyOrders(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'my_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-purchase_date')
