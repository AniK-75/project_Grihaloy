from django.urls import path
from . import views

app_name = 'heatmap'
urlpatterns = [
    path('', views.heatmap_view, name='heatmap'),
    path('get_area_data/', views.get_area_data, name='get_area_data'),

]
