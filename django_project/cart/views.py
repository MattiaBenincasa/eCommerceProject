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


#@login_required
#def remove_from_cart(request):


#@login_required
#def update_cart(request):

