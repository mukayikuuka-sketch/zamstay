# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Test endpoint
    path('test/', views.test_api, name='test-api'),
    
    # Your item endpoints
    path('items/', views.ItemListView.as_view(), name='item-list'),
    path('items/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
]