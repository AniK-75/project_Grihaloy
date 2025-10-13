from django.http import JsonResponse
from .models import HeatmapService

def heatmap_list(request):
    maps = list(HeatmapService.objects.values())
    return JsonResponse(maps, safe=False)
