import os
from django.conf import settings
from django.http import HttpResponse

class StaticDirectoryRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if request is for our specific static directory
        if request.path == '/static/zamstay-redesign/':
            # Look for redirect.html in static directories
            for static_dir in settings.STATICFILES_DIRS:
                redirect_path = os.path.join(static_dir, 'zamstay-redesign', 'redirect.html')
                if os.path.exists(redirect_path):
                    with open(redirect_path, 'r', encoding='utf-8') as f:
                        return HttpResponse(f.read())
        
        return self.get_response(request)
