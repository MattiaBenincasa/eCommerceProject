# Generated by Django 5.2.3 on 2025-06-25 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('can_view_all_customers_orders', 'può vedere gli ordini di tutti i clienti'), ('can_change_order_status', 'può cambiare lo stato di un ordine')]},
        ),
    ]
