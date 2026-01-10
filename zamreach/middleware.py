import os
from django.conf import settings
from django.http import HttpResponse

class StaticDirectoryRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if request is for our specific static directory
        if request.path == '/static/zamstay-redesign/':
            print(f'🔧 [Middleware] Handling: {request.path}')
            
            # Try to serve index.html directly
            for static_dir in settings.STATICFILES_DIRS:
                index_path = os.path.join(static_dir, 'zamstay-redesign', 'index.html')
                print(f'   Checking: {index_path}')
                if os.path.exists(index_path):
                    print(f'   ✅ Found index.html, serving it directly')
                    with open(index_path, 'r', encoding='utf-8') as f:
                        return HttpResponse(f.read(), content_type='text/html')
            
            print(f'   ❌ index.html not found')
        
        return self.get_response(request)
