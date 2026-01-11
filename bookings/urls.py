from django.urls import path
from . import views

urlpatterns = [
    path('check-homepage/', views.check_homepage, name='check_homepage'),
    # DEMO URL - for showing stakeholders
    path('demo/', views.demo_dashboard, name='demo_dashboard'),
    
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard URLs
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Public URLs
    path('', views.home, name='home'),
    path('search/', views.property_search, name='property_search'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('properties/', views.properties, name='properties'),
    
    # Owner URLs
    path('owner/properties/', views.owner_properties, name='owner_properties'),
    path('owner/property/add/', views.add_property, name='add_property'),
    path('owner/bookings/', views.owner_bookings, name='owner_bookings'),
    
    # Admin URLs
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/properties/', views.admin_properties, name='admin_properties'),
]



