# Generated by Django 5.2.3 on 2025-06-23 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_options_remove_customuser_address_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('can_access_manager_dashboard', 'Può accedere alla dashboard degli store manager')]},
        ),
    ]
