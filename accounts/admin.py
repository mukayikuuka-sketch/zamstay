from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role', 'phone_number', 'profile_image', 'bio')}),
        ('Owner Information', {'fields': ('company_name', 'tax_id')}),
        ('Guest Information', {'fields': ('nationality', 'id_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('role', 'phone_number', 'email'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
