from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)


class OutOfStockFilter(admin.SimpleListFilter):
    title = 'Disponibilità'
    parameter_name = 'stock_status'

    def lookups(self, request, model_admin):

        return (
            ('in_stock', 'Disponibile'),
            ('out_of_stock', 'Esaurito'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'out_of_stock':
            return queryset.filter(stock=0)
        if self.value() == 'in_stock':
            return queryset.filter(stock__gt=0)
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'category', OutOfStockFilter)
    list_editable = ('price', 'stock')
    raw_id_fields = ('category',)
    date_hierarchy = 'created_at'
    search_fields = ('name', 'description')



