from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime

# Simple dashboard data (for now)
def dashboard_data(request):
    """Return sample dashboard data"""
    data = {
        'stats': {
            'total_customers': 1254,
            'monthly_revenue': 45230,
            'active_promotions': 24,
            'map_views': 3456,
        },
        'recent_activities': [
            {
                'type': 'new_customer',
                'title': 'New customer registered',
                'description': 'John Doe - johndoe@example.com',
                'time': '10 minutes ago',
                'icon': 'user-plus'
            },
            {
                'type': 'promotion',
                'title': 'Promotion campaign launched',
                'description': 'Madeleine Tyson - "Summer Sale 2026"',
                'time': '25 minutes ago',
                'icon': 'bullhorn'
            },
            {
                'type': 'location',
                'title': 'New location added to map',
                'description': 'Lusaka Central - Copperbelt Region',
                'time': '1 hour ago',
                'icon': 'map-marker-alt'
            }
        ],
        'timestamp': datetime.now().isoformat(),
        'status': 'success'
    }
    return JsonResponse(data)

# Simple API views (no DRF ViewSets for now)
def get_customers(request):
    return JsonResponse({'customers': [], 'message': 'API coming soon'})

def get_promotions(request):
    return JsonResponse({'promotions': [], 'message': 'API coming soon'})

# Template views
def map_view(request):
    return render(request, 'map.html')

def analytics_view(request):
    return render(request, 'analytics.html')

def promotions_view(request):
    return render(request, 'promotions.html')

def profile_view(request):
    return render(request, 'profile.html')
