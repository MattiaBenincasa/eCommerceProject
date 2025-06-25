from django.db import models
from django.conf import settings
from products.models import Product
from addresses.models import Address


class Order(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    ORDER_STATUS_CHOICES = [
        ('Processing', 'In Lavorazione'),
        ('Shipped', 'Spedito'),
        ('Delivered', 'Consegnato'),
        ('Cancelled', 'Annullato'),
    ]

    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Processing')

    class Meta:
        permissions = [
            ('can_view_all_customers_orders', 'può vedere gli ordini di tutti i clienti'),
            ('can_change_order_status', 'può cambiare lo stato di un ordine')
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity_purchased = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'product')
