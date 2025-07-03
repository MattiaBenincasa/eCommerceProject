from django.contrib.auth.models import Group, Permission
from django.db import transaction

groups_permissions = [
    {
        'group_name': 'customer',
        'permissions': ['can_access_customer_dashboard',
                        'add_address',
                        'delete_address',
                        'view_address',
                        'change_address',
                        'can_select_address_in_checkout',
                        'view_cart',
                        'add_cartitem',
                        'change_cartitem',
                        'delete_cartitem',
                        'view_cartitem',
                        'add_order',
                        'view_order',
                        'add_orderitem',
                        'view_orderitem',
                        'add_review',
                        'delete_review',
                        'view_review',
                        'change_review']
    },
    {
        'group_name': 'store_manager',
        'permissions': ['can_access_manager_dashboard',
                        'view_customuser',
                        'can_change_order_status',
                        'can_view_all_customers_orders',
                        'view_order',
                        'add_category',
                        'view_category',
                        'change_category',
                        'delete_category',
                        'add_product',
                        'delete_product',
                        'change_product',
                        'view_product']
    },
]

with transaction.atomic():
    for group_permission in groups_permissions:
        group, created = Group.objects.get_or_create(name=group_permission['group_name'])
        permissions = Permission.objects.filter(codename__in=group_permission['permissions'])

        group.permissions.set(permissions)
        print(f"{'Creato' if created else 'Aggiornato'} il gruppo: {group.name}")

    print("Tutti i gruppi e permessi sono stati configurati correttamente.")
