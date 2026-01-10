from django.contrib import admin
from .models import Customer, Promotion, Revenue, Activity, BusinessLocation

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'location', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'location']

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title', 'promotion_type', 'status', 'start_date', 'end_date', 'budget', 'revenue_generated']
    list_filter = ['status', 'promotion_type', 'start_date']
    search_fields = ['title', 'description']

@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ['month', 'amount', 'source']
    list_filter = ['month', 'source']
    date_hierarchy = 'month'

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_type', 'description', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['activity_type', 'description']

@admin.register(BusinessLocation)
class BusinessLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_type', 'address', 'customers_count', 'is_active']
    list_filter = ['location_type', 'is_active']
    search_fields = ['name', 'address']
