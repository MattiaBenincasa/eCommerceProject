from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from .models import Cart, CartItem
from django.contrib import messages
from products.models import Product


class CartDetail(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'cart.html'
    permission_required = 'cart.view_cart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        context['cart'] = cart
        context['cart_items'] = cart_items
        context['cart_total'] = cart.calculate_total()
        return context


@require_POST
@login_required
@permission_required('cart.add_cartitem')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock > 0:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
        )
        quantity_selected = int(request.POST.get('quantity', '1'))
        if not item_created:
            if quantity_selected == 1:
                if cart_item.quantity+1 > cart_item.product.stock:
                    messages.error(request, f'Quantità di "{product.name}" non incrementata nel carrello. Stock insufficiente')
                else:
                    cart_item.quantity += 1
                    messages.success(request, f'Quantità di "{product.name}" incrementato di 1 nel carrello.')
            else:
                if quantity_selected > cart_item.product.stock:
                    messages.error(request, f'Quantità di "{product.name}" non aggiornata nel carrello. Stock insufficiente')
                else:
                    cart_item.quantity = quantity_selected
                    messages.success(request, f'Quantità di "{product.name}" aggiornata nel carrello.')
        else:
            if quantity_selected > product.stock:
                messages.error(request, f'"{product.name}" non aggiunti al carrello per stock insufficiente')
            else:
                cart_item.quantity = quantity_selected
                messages.success(request, f'"{product.name}" aggiunto al carrello.')

        cart_item.save()
    else:
        messages.error(request, 'Prodotto non disponibile')

    # includo i parametri della ricerca in modo che, dopo l'aggiunta del prodotto
    # il cliente possa tornare alla pagina dei prodotti con i parametri del form precedenti
    search_params = request.POST.get('redirect_params', '')
    redirect_url = reverse_lazy('product_details', kwargs={'slug': product.slug})
    print(search_params)
    if search_params:
        redirect_url = f"{redirect_url}?{search_params}"

    return redirect(redirect_url)


@require_POST
@login_required
@permission_required('cart.delete_cartitem')
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    return redirect('cart')


@require_POST
@login_required
@permission_required('cart.change_cartitem')
def increment_item_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if cart_item.quantity+1 > cart_item.product.stock:
        cart_item.quantity = cart_item.product.stock
    else:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@require_POST
@login_required
@permission_required('cart.change_cartitem')
def decrement_item_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if cart_item.quantity-1 <= 0:
        remove_from_cart(request, item_id)
    else:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')
