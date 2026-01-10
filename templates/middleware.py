# zamreach/middleware.py
from django.http import HttpResponse
import os
from django.conf import settings

class StaticDirectoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if this is exactly /static/zamstay-redesign/ (not /static/zamstay-redesign/filename)
        if request.path == '/static/zamstay-redesign/':
            # Try to find and serve index.html
            for static_dir in settings.STATICFILES_DIRS:
                index_path = os.path.join(static_dir, 'zamstay-redesign', 'index.html')
                if os.path.exists(index_path):
                    with open(index_path, 'r', encoding='utf-8') as f:
                        return HttpResponse(f.read(), content_type='text/html')
        
        return self.get_response(request)
