from django.urls import path
from . import views

urlpatterns = [
    path('', views.trend_list, name='trend_list'),
]
