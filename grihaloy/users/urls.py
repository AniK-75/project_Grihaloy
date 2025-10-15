from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # --- Auth ---
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # --- NEW: Profile URLs ---
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),

    # --- NEW: Admin User Management ---
    path('admin/users/', views.user_list, name='user_list'),
    path('admin/users/approve/<int:pk>/', views.approve_user, name='approve_user'),

    # --- Verification ---
    path('verification/', views.verification_list, name='verification_list'),
    path('verification/upload/', views.verification_create, name='verification_create'),
    path('verification/delete/<int:pk>/', views.verification_delete, name='verification_delete'),
    path('verification/<int:pk>/status/<str:status>/', views.verification_change_status,
         name='verification_change_status'),

    # --- Ratings ---
    path('ratings/<int:user_id>/', views.rating_list, name='rating_list'),
    path('ratings/add/<int:rated_id>/', views.rating_create, name='rating_create'),
]
