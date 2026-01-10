from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include bookings app URLs - THIS FIXES THE DASHBOARD ISSUE!
    path('', include('bookings.urls')),
]
