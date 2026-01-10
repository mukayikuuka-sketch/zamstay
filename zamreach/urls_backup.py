from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

def static_directory_view(request):
    return HttpResponse("Static files at /static/", content_type='text/plain')

urlpatterns = [
    path('', include('bookings.urls')),
    path('owner/', RedirectView.as_view(url='/owner/dashboard/')),
    # Django Admin
    path('admin/', admin.site.urls),

    # Your existing API endpoints
    path('api/', include('api.urls')),

    # Business Ads API (SIMPLIFIED)
    path('api/business/', include('business_ads.urls')),

    # Static directory info
    path('static/', static_directory_view, name='static_directory'),

    # FAVICON - must come before catch-all
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),

    # ========== ZAMSTAY OWNER ROUTES ==========
    # Owner Dashboard
    path('owner/', TemplateView.as_view(template_name='owner-dashboard.html'), name='owner_dashboard'),
    
    # Owner Pages
    path('owner/properties/', TemplateView.as_view(template_name='properties.html'), name='properties'),
    path('owner/bookings/', TemplateView.as_view(template_name='bookings.html'), name='bookings'),
    path('owner/maintenance/', TemplateView.as_view(template_name='maintenance.html'), name='maintenance'),
    path('owner/staff/', TemplateView.as_view(template_name='staff.html'), name='staff'),
    path('owner/financials/', TemplateView.as_view(template_name='financials.html'), name='financials'),
    path('owner/profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),

    # ========== ZAMSTAY GUEST ROUTES ==========
    # Guest Portal
    path('guest/', TemplateView.as_view(template_name='guest-portal.html'), name='guest_portal'),
    
    # Guest Pages
    path('guest/search/', TemplateView.as_view(template_name='search.html'), name='search'),
    path('guest/trips/', TemplateView.as_view(template_name='trips.html'), name='trips'),
    path('guest/saved/', TemplateView.as_view(template_name='saved.html'), name='saved'),
    path('guest/profile/', TemplateView.as_view(template_name='guest-profile.html'), name='guest_profile'),
    path('guest/property/<int:property_id>/', TemplateView.as_view(template_name='property-detail.html'), name='property_detail'),
    path('guest/booking/<int:booking_id>/', TemplateView.as_view(template_name='booking-flow.html'), name='booking_flow'),

    # ========== LEGACY ZAMREACH ROUTES (keep for compatibility) ==========
    path('map/', TemplateView.as_view(template_name='map.html'), name='map'),
    path('analytics/', TemplateView.as_view(template_name='analytics.html'), name='analytics'),
    path('promotions/', TemplateView.as_view(template_name='promotions.html'), name='promotions'),
    
    # Root URL - redirect based on user role
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]

# Catch-all for SPA (MUST BE LAST)
urlpatterns.append(
    path('<path:route>', TemplateView.as_view(template_name='index.html'))
)

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

