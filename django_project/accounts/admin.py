from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser

# Register your models here.

'''
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': 'birth_date'}),
    )
    list_display = UserAdmin.list_display
    list_filter = UserAdmin.list_filter
    search_fields = UserAdmin.search_fields


admin.site.register(CustomUser, CustomUserAdmin)'''

