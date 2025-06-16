from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from django.contrib import messages
from products.models import Product


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'title': 'Il Mio Carrello' # Title for the template
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not item_created:
        cart_item.quantity += 1
        messages.success(request, f'Quantità di "{product.name}" aggiornata nel carrello.')
    else:
        messages.success(request, f'"{product.name}" aggiunto al carrello.')

    cart_item.save()

    return redirect('cart',)


@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item_name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f'"{item_name}" rimosso dal carrello.')
    return redirect('cart')


@login_required
def increment_item_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if cart_item.quantity+1 > cart_item.product.stock:
        cart_item.quantity = cart_item.product.stock
    else:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def decrement_item_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if cart_item.quantity-1 <= 0:
        remove_from_cart(request, item_id)
    else:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')
