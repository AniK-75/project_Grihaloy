from django.urls import path
from .views import (
    PropertyListView, PropertyDetailView,
    PropertyCreateView, PropertyUpdateView, PropertyDeleteView,
    MyPropertyListView, property_activate, property_deactivate,
    property_photo_delete, request_edit, request_delete,
    edit_request_list, approve_edit_request, reject_edit_request,
    approve_delete_request, reject_delete_request, notifications,
    start_negotiation, negotiation_chat, my_negotiations # NEW
)

app_name = 'properties'

urlpatterns = [
    path('', PropertyListView.as_view(), name='list'),
    path('my/', MyPropertyListView.as_view(), name='my'),
    path('add/', PropertyCreateView.as_view(), name='add'),
    path('<uuid:pk>/', PropertyDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', PropertyUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', PropertyDeleteView.as_view(), name='delete'),

    path('<uuid:pk>/deactivate/', property_deactivate, name='deactivate'),
    path('<uuid:pk>/activate/', property_activate, name='activate'),
    path('<uuid:pk>/photos/<uuid:photo_id>/delete/', property_photo_delete, name='photo_delete'),

    path('<uuid:pk>/request-edit/', request_edit, name='request_edit'),
    path('<uuid:pk>/request-delete/', request_delete, name='request_delete'),

    path('requests/', edit_request_list, name='requests'),
    path('requests/edit/<uuid:request_id>/approve/', approve_edit_request, name='approve_edit_request'),
    path('requests/edit/<uuid:request_id>/reject/', reject_edit_request, name='reject_edit_request'),
    path('requests/delete/<uuid:request_id>/approve/', approve_delete_request, name='approve_delete_request'),
    path('requests/delete/<uuid:request_id>/reject/', reject_delete_request, name='reject_delete_request'),

    path('notifications/', notifications, name='notifications'),

    # NEW: Negotiation Paths
    path('<uuid:pk>/negotiate/', start_negotiation, name='start_negotiation'),
    path('negotiation/<uuid:pk>/', negotiation_chat, name='negotiation_chat'),
    path('my-negotiations/', my_negotiations, name='my_negotiations'),
]