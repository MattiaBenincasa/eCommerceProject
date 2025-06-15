from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birth_date', 'country', 'city', 'address', 'postcode')}),
    )
    list_display = UserAdmin.list_display + ('birth_date', 'country', 'city', 'address', 'postcode')
    list_filter = UserAdmin.list_filter + ('country', 'city')
    search_fields = UserAdmin.search_fields + ('country', 'city', 'address')


admin.site.register(CustomUser, CustomUserAdmin)

