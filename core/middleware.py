from django.shortcuts import redirect
from django.urls import reverse


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