def custom_tabs(request):
    """
    Makes estate-specific custom tabs available in every template.
    Returns an empty list if user is not authenticated or no tabs exist.
    """
    tabs = []

    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            if profile and profile.estate:
                from .models import CustomTab
                tabs = CustomTab.objects.filter(
                    estate=profile.estate,
                    is_active=True
                ).order_by('created_at')
        except Exception:
            pass

    return {'custom_tabs': tabs}