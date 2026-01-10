from django.urls import path
from . import views

urlpatterns = [
    # Simple API endpoints
    path('dashboard/data/', views.dashboard_data, name='dashboard_data'),
    path('customers/', views.get_customers, name='customers'),
    path('promotions/', views.get_promotions, name='promotions'),
    
    # Note: We're NOT using the template views here since they're in main urls.py
]
