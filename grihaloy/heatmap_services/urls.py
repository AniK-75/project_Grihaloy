from django.urls import path
from . import views

urlpatterns = [
    path('', views.heatmap_list, name='heatmap_list'),
]
