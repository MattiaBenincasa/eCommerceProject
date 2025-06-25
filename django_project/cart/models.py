from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        unique=True,
    )

    @property
    def is_empty(self):
        return self.cartitem_set.count() == 0

    def calculate_total(self):
        cart_items = CartItem.objects.filter(cart=self)
        return sum(item.product.price * item.quantity for item in cart_items)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)
