from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer, Promotion, Revenue, Activity, BusinessLocation

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'location', 'status', 'created_at']

class PromotionSerializer(serializers.ModelSerializer):
    roi = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Promotion
        fields = ['id', 'title', 'description', 'promotion_type', 'status', 
                 'start_date', 'end_date', 'budget', 'reach', 'conversions',
                 'revenue_generated', 'roi', 'is_active', 'created_at']

class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ['id', 'month', 'amount', 'source']

class ActivitySerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['id', 'activity_type', 'description', 'icon', 'time_ago', 'created_at']
    
    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"

class BusinessLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessLocation
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 
                 'location_type', 'customers_count', 'is_active']

class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_customers = serializers.IntegerField()
    monthly_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    active_promotions = serializers.IntegerField()
    total_locations = serializers.IntegerField()
    recent_activities = ActivitySerializer(many=True)
