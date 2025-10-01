from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, VerificationDocument, Rating

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields':('role','phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields':('role','phone')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VerificationDocument)
admin.site.register(Rating)
