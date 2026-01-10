from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Property, Booking, Review
from django.contrib.auth.models import User

# PUBLIC/CUSTOMER VIEWS
def home(request):
    """Customer homepage - search for properties"""
    properties = Property.objects.filter(is_active=True)[:6]
    return render(request, 'customer/home.html', {
        'properties': properties,
        'user_role': 'customer'
    })

def property_search(request):
    """Search properties by location, dates, etc."""
    location = request.GET.get('location', '')
    properties = Property.objects.filter(is_active=True)
    
    if location:
        properties = properties.filter(location__icontains=location)
    
    return render(request, 'customer/search.html', {
        'properties': properties,
        'search_query': location
    })

def property_detail(request, property_id):
    """View property details"""
    property = get_object_or_404(Property, id=property_id, is_active=True)
    return render(request, 'customer/property_detail.html', {
        'property': property
    })

@login_required
def create_booking(request, property_id):
    """Create a booking for a property"""
    property = get_object_or_404(Property, id=property_id, is_active=True)
    
    if request.method == 'POST':
        # Process booking form
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        guests = request.POST.get('guests', 1)
        
        # Calculate price
        nights = (check_out - check_in).days
        total_price = property.price_per_night * nights
        
        booking = Booking.objects.create(
            customer=request.user,
            property=property,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            status='pending'
        )
        
        return redirect('booking_confirmation', booking_id=booking.id)
    
    return render(request, 'customer/create_booking.html', {
        'property': property
    })

@login_required
def my_bookings(request):
    """View customer's bookings"""
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'customer/my_bookings.html', {
        'bookings': bookings
    })

# OWNER VIEWS
@login_required
def owner_dashboard(request):
    """Owner dashboard - shows stats for their properties"""
    properties = Property.objects.filter(owner=request.user)
    bookings = Booking.objects.filter(property__owner=request.user)
    
    # Calculate stats
    total_revenue = sum(b.total_price for b in bookings.filter(status='confirmed'))
    active_bookings = bookings.filter(status='confirmed').count()
    pending_bookings = bookings.filter(status='pending').count()
    
    return render(request, 'owner/dashboard.html', {
        'properties': properties,
        'total_revenue': total_revenue,
        'active_bookings': active_bookings,
        'pending_bookings': pending_bookings,
        'user_role': 'owner'
    })

@login_required
def owner_properties(request):
    """List all properties owned by user"""
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'owner/properties.html', {
        'properties': properties
    })

@login_required
def add_property(request):
    """Add new property"""
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        price_per_night = request.POST.get('price_per_night')
        
        property = Property.objects.create(
            owner=request.user,
            name=name,
            location=location,
            price_per_night=price_per_night,
            is_active=True
        )
        
        return redirect('owner_properties')
    
    return render(request, 'owner/add_property.html')

@login_required
def owner_bookings(request):
    """View bookings for owner's properties"""
    bookings = Booking.objects.filter(property__owner=request.user).order_by('-created_at')
    return render(request, 'owner/bookings.html', {
        'bookings': bookings
    })

# ADMIN VIEWS
@staff_member_required
def admin_dashboard(request):
    """Admin dashboard - platform overview"""
    total_users = User.objects.count()
    total_properties = Property.objects.count()
    total_bookings = Booking.objects.count()
    
    return render(request, 'admin/dashboard.html', {
        'total_users': total_users,
        'total_properties': total_properties,
        'total_bookings': total_bookings,
        'user_role': 'admin'
    })

@staff_member_required
def admin_users(request):
    """Admin user management"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin/users.html', {
        'users': users
    })

@staff_member_required
def admin_properties(request):
    """Admin property management"""
    properties = Property.objects.all().order_by('-created_at')
    return render(request, 'admin/properties.html', {
        'properties': properties
    })

