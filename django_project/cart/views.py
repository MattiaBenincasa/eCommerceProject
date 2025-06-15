from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cart
# Create your views here.


@login_required
def cart_detail(request):
    cart_items = Cart.objects.all()

    context = {
        'cart': Cart,
        'cart_items': cart_items,
        'title': 'Il Mio Carrello'
    }
    return render(request, 'cart.html', context)

