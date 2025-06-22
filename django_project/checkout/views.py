from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from .forms import CheckoutAddressForm, PaymentForm
from addresses.forms import AddressForm
from products.models import Product
from cart.models import Cart, CartItem
from addresses.models import Address
from django.contrib import messages
from orders.models import Order, OrderItem


class CheckoutAddressSelectionView(LoginRequiredMixin, FormView):
    template_name = 'checkout/address_selection_checkout.html'
    form_class = CheckoutAddressForm
    success_url = reverse_lazy('process_order')

    def get_initial(self):
        initial = super().get_initial()
        address_id = self.request.session.pop('id_last_address_added', None)
        if address_id:
            user_address = get_object_or_404(Address, user=self.request.user, id=address_id)
        else:
            user_address = get_object_or_404(Address, user=self.request.user, is_main=True)
        initial['existing_addresses'] = user_address
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        context['cart_items'] = cart_items
        context['cart_total'] = cart.total_amount
        return context

    def form_valid(self, form):
        selected_address_obj = form.cleaned_data['existing_addresses']
        self.request.session['shipping_address_id'] = selected_address_obj.id
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Si prega di selezionare un indirizzo valido.')


class CheckoutAddressCreationView(LoginRequiredMixin, FormView):
    template_name = 'checkout/address_creation_checkout.html'
    form_class = AddressForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        context['cart_items'] = cart_items
        context['cart_total'] = cart.total_amount
        return context

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        self.request.session['id_last_address_added'] = address.id
        return redirect('address_selection')


class ProcessOrderView(LoginRequiredMixin, FormView):
    template_name = 'checkout/payment_methods_checkout.html'
    form_class = PaymentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        context['cart_items'] = cart_items
        context['cart_total'] = cart.total_amount
        return context

    def form_valid(self, form):
        cart = get_object_or_404(Cart, user=self.request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        shipping_address = get_object_or_404(Address, id=self.request.session['shipping_address'], user=self.request.user)

        order_items_to_create = []
        products_to_update = []

        try:
            with transaction.atomic():
                order = Order.objects.create(customer=self.request.user, shipping_address=shipping_address)
                print(f"Contenuto di cart_items: {cart_items}")

                for cart_item in cart_items:
                    product = cart_item.product
                    quantity = cart_item.quantity

                    if product.stock < quantity:
                        messages.error(self.request,
                                       f"Quantità insufficiente per '{product.name}'. Stock disponibile: {product.stock}")
                        raise ValueError("Stock insufficiente")

                    order_items_to_create.append(
                        OrderItem(
                            order=order,
                            product=product,
                            quantity_purchased=quantity,
                            price_at_purchase=product.price
                        )
                    )
                    product.stock -= quantity
                    products_to_update.append(product)

                OrderItem.objects.bulk_create(order_items_to_create)
                Product.objects.bulk_update(products_to_update, ['stock'])
                order.save()
                cart_items.delete()
                if 'shipping_address_id' in self.request.session:
                    del self.request.session['shipping_address_id']
                return redirect('order_confirmation', order_id=order.id)

        except ValueError as e:
            messages.error(self.request, f"Errore durante l'elaborazione dell'ordine: {e}")
            print(f"Errore 1: {e}")
            return redirect('checkout')

        except Exception as e:
            messages.error(self.request, f"Si è verificato un errore inaspettato: {e}. Riprova.")
            print(f"Errore 2: {e}")
            return redirect('checkout')


class OrderConfirmation(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'checkout/order_confirmation.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['order_items'] = OrderItem.objects.filter(order=order)
        context['title'] = f'Conferma Ordine #{order.id}'
        return context
