from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Simple health check endpoint for Railway
def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ip', health_check, name='health-check'),  # For Railway health checks
    path('health', health_check, name='health'),    # Alternative endpoint
    path('', include('bookings.urls')),
]
