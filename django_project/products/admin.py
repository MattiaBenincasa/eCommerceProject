from django.contrib import admin
from .models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'category')
    list_editable = ('price', 'stock')
    raw_id_fields = ('category',)
    date_hierarchy = 'created_at'
    search_fields = ('name', 'description')
