from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Address
from .forms import AddressForm


class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'addresses/address_list.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).order_by('-is_main', 'city')


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'addresses/address_form.html'
    success_url = reverse_lazy('address_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        return response


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'addresses/address_form.html'
    success_url = reverse_lazy('address_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        set_first_object_main(self.get_object(), self.request.user)
        response = super().form_valid(form)
        return response


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = 'addresses/address_confirm_delete.html'
    success_url = reverse_lazy('address_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        set_first_object_main(self.get_object(), self.request.user)
        response = super().form_valid(form)
        return response


# quando canello o modifico un indirizzo, se quell'indirizzo ero quello principale,
# questa funzione mi setta il primo indirizzo della lista come main
@login_required
def set_first_object_main(address, user):
    if address.is_main:
        other_addresses = Address.objects.filter(user=user).exclude(pk=address.pk)
        if other_addresses.exists():
            # se non ho altri main address allora faccio diventare il primo indirizzo main address
            first_other_address = other_addresses.first()
            first_other_address.is_main = True
            first_other_address.save()
