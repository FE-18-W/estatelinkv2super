from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.cache import never_cache


class AdminAccessMiddleware:
    """
    Controls access to Django admin panel.
    - SUPERUSERS: Always allowed, never blocked
    - STAFF (estate admins): Allowed with estate-scoped data
    - REGULAR USERS: Blocked with friendly message
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            # Not authenticated → send to login
            if not request.user.is_authenticated:
                return redirect(reverse('login'))
            
            # SUPERUSER → ALWAYS ALLOW, NEVER BLOCK
            if request.user.is_superuser:
                response = self.get_response(request)
                return response
            
            # Staff (estate admins) → allowed
            if request.user.is_staff:
                response = self.get_response(request)
                return response
            
            # Regular users → blocked
            return redirect(reverse('access_denied'))

        response = self.get_response(request)
        return response


class NoAuthCacheMiddleware:
    """
    Prevents caching of authenticated pages to ensure users cannot access
    protected content after logout. Sets cache-control headers to prevent
    browser from caching pages that require authentication.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # For authenticated pages, prevent all caching
        if request.user.is_authenticated:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response