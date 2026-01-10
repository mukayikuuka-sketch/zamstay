from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Property, Booking, Review

# ==================== CUSTOMER PAGES (REDESIGN) ====================

def home(request):
    """Home page - using ZamStay Redesign with apartments/hotels/lodges"""
    # Option 1: Use the ZamStay redesign static file (has all 3 categories)
    return render(request, 'customer/home.html')
    # Option 2: Or use the property-detail.html template if you want Django template
    # return render(request, 'property-detail.html')

def property_search(request):
    """Property search page - using customer/search.html"""
    return render(request, 'customer/search.html')

def property_detail(request, property_id):
    """Property detail page - using the FULL booking system template"""
    return render(request, 'property-detail.html', {'property_id': property_id})

def properties(request):
    """Properties page - simple redirect to search for now"""
    return redirect('property_search')

def about(request):
    """About page"""
    # If about.html doesn't exist, redirect to home
    return redirect('/')

def contact(request):
    """Contact page"""
    # If contact.html doesn't exist, redirect to home
    return redirect('/')

def faq(request):
    """FAQ page"""
    # If faq.html doesn't exist, redirect to home
    return redirect('/')

@login_required
def customer_dashboard(request):
    """Customer dashboard - using guest portal redesign"""
    return render(request, 'guest-portal.html', {'user': request.user})

# ==================== AUTHENTICATION ====================

def signup_view(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    """User login"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """User logout"""
    logout(request)
    return redirect('home')

# ==================== DASHBOARDS ====================

@login_required
def owner_dashboard(request):
    """Owner dashboard"""
    return render(request, 'owner/dashboard.html')

@login_required 
def admin_dashboard(request):
    """Admin dashboard"""
    return render(request, 'admin/dashboard.html')

# ==================== OWNER PAGES ====================

@login_required
def owner_properties(request):
    """Owner properties management"""
    return render(request, 'owner/properties.html')

@login_required
def add_property(request):
    """Add new property"""
    return render(request, 'owner/add_property.html')

@login_required
def owner_bookings(request):
    """Owner bookings management"""
    return render(request, 'owner/bookings.html')

# ==================== ADMIN PAGES ====================

@login_required
def admin_users(request):
    """Admin user management"""
    return render(request, 'admin/users.html')

@login_required
def admin_properties(request):
    """Admin properties management"""
    return render(request, 'admin/properties.html')

# ==================== DEMO ====================

def demo_dashboard(request):
    """Demo dashboard for stakeholders"""
    return render(request, 'unified_dashboard.html')

