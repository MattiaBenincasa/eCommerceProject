from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import DetailView
from .forms import PaymentForm
from .models import Order, OrderItem
from cart.models import Cart, CartItem


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.warning(request, "Il tuo carrello è vuoto. Aggiungi prodotti prima di procedere al checkout.")
        return redirect('cart')
    print(cart.total_amount)
    form = PaymentForm()
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart.total_amount,
        'form': form,
        'title': 'Checkout'
    }
    return render(request, 'checkout.html', context)


def process_order(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items:
            messages.warning(request, "Il tuo carrello è vuoto. Impossibile creare un ordine.")
            return redirect('cart')

        if form.is_valid():
            # assumo che il pagamento sia andato a buon fine
            order_items_to_create = []
            products_to_update = []

            try:
                with transaction.atomic():
                    order = Order.objects.create(customer=request.user)

                    for cart_item in cart_items:
                        product = cart_item.product
                        quantity = cart_item.quantity

                        if product.stock < quantity:
                            messages.error(request, f"Quantità insufficiente per '{product.name}'. Disponibile: {product.stock}, Richiesto: {quantity}.")
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
                    order.total_amount = cart.total_amount
                    order.save()
                    cart_items.delete()
                    print("pagamento riuscito")

                messages.success(request, f"Ordine #{order.id} creato con successo! I dettagli del tuo ordine sono disponibili nella tua dashboard.")

            except ValueError as e:
                messages.error(request, f"Errore durante l'elaborazione dell'ordine: {e}")
                print("Errore 1")
                return redirect('checkout')
            except Exception as e:
                messages.error(request, f"Si è verificato un errore inaspettato: {e}. Riprova più tardi.")
                print("Errore 2")
                return redirect('checkout')
        else:
            messages.error(request, "Si prega di correggere gli errori nel form di pagamento.")
            cart_total = cart.total_amount
            context = {
                'cart': cart,
                'cart_items': cart_items,
                'cart_total': cart_total,
                'form': form,
                'title': 'Checkout'
            }
            print("errore 3")
            return render(request, 'checkout.html', context)
        return redirect('order_confirmation', order_id=order.id)
    else:
        print("Errore 4")
        return redirect('checkout')


class OrderConfirmation(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_confirmation.html'
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

