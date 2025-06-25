from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Order


class MyOrders(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Order
    template_name = 'my_orders.html'
    context_object_name = 'orders'
    permission_required = 'orders.view_order'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-purchase_date')


class OrderDetails(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_details.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
    permission_required = 'orders.view_order'

    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)
