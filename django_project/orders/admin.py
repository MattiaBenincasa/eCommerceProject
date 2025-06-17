from django.contrib import admin
from django.contrib import messages
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'purchase_date',
        'total_amount',
        'status_display',
    )

    list_filter = (
        'status',
        'purchase_date',
        'customer',
    )

    search_fields = (
        'id__exact',
        'customer__username__icontains',
        'customer__first_name__icontains',
        'customer__last_name__icontains',
        'status',
    )

    # Campi non modificabili (readonly) per evitare modifiche accidentali
    readonly_fields = (
        'purchase_date',
        'total_amount',
        'customer',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def status_display(self, obj):
        return obj.get_status_display()

    status_display.short_description = 'Stato'

    @admin.action(description="Segna ordini come 'In Lavorazione'")
    def mark_as_processing(self, request, queryset):
        updated_count = queryset.update(status='Processing')
        self.message_user(request, f"{updated_count} ordini sono stati segnati come 'In Lavorazione'.",
                          messages.success)

    @admin.action(description="Segna ordini come 'Spedito'")
    def mark_as_shipped(self, request, queryset):
        updated_count = queryset.update(status='Shipped')
        self.message_user(request, f"{updated_count} ordini sono stati segnati come 'Spedito'.", 'success')

    @admin.action(description="Segna ordini come 'Consegnato'")
    def mark_as_delivered(self, request, queryset):
        updated_count = queryset.update(status='Delivered')
        self.message_user(request, f"{updated_count} ordini sono stati segnati come 'Consegnato'.", 'success')

    @admin.action(description="Segna ordini come 'Annullato'")
    def mark_as_cancelled(self, request, queryset):
        updated_count = queryset.update(status='Cancelled')
        self.message_user(request, f"{updated_count} ordini sono stati segnati come 'Annullato'.", messages.warning)

    actions = [
        'mark_as_processing',
        'mark_as_shipped',
        'mark_as_delivered',
        'mark_as_cancelled',
    ]
