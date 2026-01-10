from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect

def demo_view(request):
    """Render the unified dashboard"""
    return render(request, "owner-dashboard.html")

def redirect_to_demo(request):
    """Redirect any /owner/ route to demo"""
    return redirect('/demo/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', demo_view, name='demo'),
    path('owner/', redirect_to_demo),  # Redirect /owner/ to demo
    path('owner/dashboard/', redirect_to_demo),  # Redirect /owner/dashboard/ to demo
    path('', demo_view),  # Root goes to demo
]
