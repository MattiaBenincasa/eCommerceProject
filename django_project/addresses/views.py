from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Address
from .forms import AddressForm


class AddressListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Address
    permission_required = 'addresses.view_address'
    template_name = 'addresses/address_list.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).order_by('-is_main', 'city')


class AddressCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Address
    permission_required = 'addresses.add_address'
    form_class = AddressForm
    template_name = 'addresses/address_form.html'
    success_url = reverse_lazy('address_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddressUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Address
    permission_required = 'addresses.change_address'
    form_class = AddressForm
    template_name = 'addresses/address_form.html'
    success_url = reverse_lazy('address_list')


class AddressDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Address
    permission_required = 'addresses.delete_address'
    template_name = 'addresses/address_confirm_delete.html'
    success_url = reverse_lazy('address_list')
