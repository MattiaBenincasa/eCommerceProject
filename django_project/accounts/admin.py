from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.models import Group
from django.contrib import messages


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_readonly_fields(self, request, obj=None):
        default_readonly = ('last_login',
                            'date_joined',
                            'email',
                            'first_name',
                            'last_name',
                            'user_permissions',
                            'is_staff',
                            'groups'
                            )

        if obj:
            customer_group = Group.objects.get(name='customer')
            if customer_group in obj.groups.all():
                return default_readonly + ('is_superuser', 'username')

        return default_readonly

    def save_model(self, request, obj, form, change):
        if not change and request.user.is_superuser:
            store_manager_group = Group.objects.get(name='store_manager')
            obj.is_staff = True
            obj.is_superuser = False
            obj.is_active = True

            super().save_model(request, obj, form, change)

            obj.groups.add(store_manager_group)

            messages.success(request, f"Utente '{obj.username}' creato come Store Manager.")
            return

        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        if obj and request.user.is_superuser:
            customer_group = Group.objects.get(name='customer')
            if customer_group in obj.groups.all():
                return False

        return super().has_delete_permission(request, obj)

    def add_view(self, request, form_url="", extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Aggiungi Store Manager"
        return super().add_view(request, form_url, extra_context)


admin.site.register(CustomUser, CustomUserAdmin)

