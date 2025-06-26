from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from django.utils import timezone
from datetime import timedelta
from .forms import OrderFilterForm, OrderStatusForm, MyOrderFilter
from .models import Order
from django.db.models import Q


class MyOrders(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Order
    template_name = 'my_orders.html'
    context_object_name = 'orders'
    permission_required = 'orders.view_order'
    paginate_by = 10
    form = MyOrderFilter()

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-purchase_date')
        self.form = MyOrderFilter(self.request.GET)

        if self.form.is_valid():
            order_number_str = self.form.cleaned_data.get('order_number')
            status_filter = self.form.cleaned_data.get('status_filter')
            sort_by = self.form.cleaned_data.get('sort_by')

            if order_number_str:
                try:
                    order_number = int(order_number_str)
                    queryset = queryset.filter(id=order_number)
                except ValueError:
                    pass

            if status_filter:
                queryset = queryset.filter(status=status_filter)

            if sort_by:
                if sort_by == 'latest':
                    queryset = queryset.order_by('-purchase_date')
                elif sort_by == 'earliest':
                    queryset = queryset.order_by('purchase_date')

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context


class OrderDetails(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_details.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
    permission_required = 'orders.view_order'

    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)


class CustomersOrders(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Order
    permission_required = 'orders.can_view_all_customers_orders'
    template_name = 'store_manager/customers_orders.html'
    context_object_name = 'orders'
    paginate_by = 10
    form = OrderFilterForm()

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-purchase_date')
        self.form = OrderFilterForm(self.request.GET)

        if self.form.is_valid():
            date_filter = self.form.cleaned_data.get('date_filter')
            customer_query = self.form.cleaned_data.get('customer_query')
            order_number_str = self.form.cleaned_data.get('order_number')
            status_filter = self.form.cleaned_data.get('status_filter')
            sort_by = self.form.cleaned_data.get('sort_by')

            if date_filter:
                today = timezone.now().date()
                if date_filter == 'today':
                    queryset = queryset.filter(purchase_date__date=today)
                elif date_filter == 'last_week':
                    start_date = today - timedelta(days=7)
                    queryset = queryset.filter(purchase_date__date__range=[start_date, today])
                elif date_filter == 'last_month':
                    start_date = today - timedelta(days=30)
                    queryset = queryset.filter(purchase_date__date__range=[start_date, today])

            if customer_query:
                queryset = queryset.filter(
                    Q(customer__first_name__icontains=customer_query) |
                    Q(customer__last_name__icontains=customer_query) |
                    Q(customer__username__icontains=customer_query)
                )

            if order_number_str:
                try:
                    order_number = int(order_number_str)
                    queryset = queryset.filter(id=order_number)
                except ValueError:
                    pass

            if status_filter:
                queryset = queryset.filter(status=status_filter)

            if sort_by:
                if sort_by == 'latest':
                    queryset = queryset.order_by('-purchase_date')
                elif sort_by == 'earliest':
                    queryset = queryset.order_by('purchase_date')

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context


class ChangeOrderStatus(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Order
    permission_required = 'orders.can_change_order_status'
    context_object_name = 'order'
    form_class = OrderStatusForm
    template_name = 'store_manager/change_order_status.html'
    success_url = reverse_lazy('customers_orders')

