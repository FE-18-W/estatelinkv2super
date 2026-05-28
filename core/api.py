from django.http import JsonResponse
from .models import SecurityAlert

def latest_alert_count(request):
    estate_id = request.GET.get('estate')
    count = SecurityAlert.objects.filter(estate_id=estate_id, created_at__gte=timezone.now()-timezone.timedelta(minutes=5)).count()
    return JsonResponse({'count': count})