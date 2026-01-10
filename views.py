from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

# SIMPLIFIED VIEWS FOR DEMO

def demo_dashboard(request):
    """Demo dashboard showing all user roles"""
    return render(request, 'owner-dashboard.html')

def home(request):
    """Home page - redirects to demo"""
    return redirect('demo_dashboard')

def property_search(request):
    """Property search - demo version"""
    return render(request, 'demo_search.html')

def property_detail(request, property_id):
    """Property detail - demo version"""
    return render(request, 'demo_property.html')

# Simple placeholder views for demo
def signup_view(request):
    """Demo signup - redirects to demo"""
    return redirect('demo_dashboard')

def login_view(request):
    """Demo login - redirects to demo"""
    return redirect('demo_dashboard')

def logout_view(request):
    """Demo logout - redirects to demo"""
    return redirect('demo_dashboard')

def customer_dashboard(request):
    """Customer dashboard - demo version"""
    return redirect('demo_dashboard')

def owner_dashboard(request):
    """Owner dashboard - demo version"""
    return redirect('demo_dashboard')

def admin_dashboard(request):
    """Admin dashboard - demo version"""
    return redirect('demo_dashboard')

def owner_properties(request):
    """Owner properties - demo version"""
    return render(request, 'demo_owner_properties.html')

def add_property(request):
    """Add property - demo version"""
    return render(request, 'demo_add_property.html')

def owner_bookings(request):
    """Owner bookings - demo version"""
    return render(request, 'demo_owner_bookings.html')

def admin_users(request):
    """Admin users - demo version"""
    return render(request, 'demo_admin_users.html')

def admin_properties(request):
    """Admin properties - demo version"""
    return render(request, 'demo_admin_properties.html')
