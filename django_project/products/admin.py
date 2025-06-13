from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'category')
    list_editable = ('price', 'stock')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category',)
    date_hierarchy = 'created_at'
    search_fields = ('name', 'description')
