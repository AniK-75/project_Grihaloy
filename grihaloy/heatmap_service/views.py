from django.http import JsonResponse
from django.shortcuts import render
from .models import AreaHeatmap

def heatmap_view(request):
    return render(request, 'heatmap_service/heatmap.html')

def get_area_data(request):
    data = [
        {
            "area": h.area,
            "avg_price": h.avg_price,
            "color": h.color
        }
        for h in AreaHeatmap.objects.all()

    ]


    return JsonResponse(data, safe=False)
