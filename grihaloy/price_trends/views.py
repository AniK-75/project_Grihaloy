from django.http import JsonResponse
from .models import PriceTrend

def trend_list(request):
    trends = list(PriceTrend.objects.values())
    return JsonResponse(trends, safe=False)
