from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('verification/', views.verification_list, name='verification_list'),
    path('verification/upload/', views.verification_create, name='verification_create'),
    path('verification/delete/<int:pk>/', views.verification_delete, name='verification_delete'),
    path('verification/<int:pk>/status/<str:status>/', views.verification_change_status, name='verification_change_status'),

    path('ratings/<int:user_id>/', views.rating_list, name='rating_list'),
    path('ratings/add/<int:rated_id>/', views.rating_create, name='rating_create'),
]
