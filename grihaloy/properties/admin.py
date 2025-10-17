from django.contrib import admin
from django.utils import timezone
from .models import Property, PropertyPhoto, PropertyEditRequest, PropertyDeleteRequest

class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto
    extra = 1
    fields = ('image', 'caption', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'city', 'area', 'property_type', 'price', 'is_price_fixed', 'is_active', 'owner_can_edit', 'created_at')
    list_filter = ('city', 'area', 'property_type', 'is_active', 'is_price_fixed', 'owner_can_edit')
    search_fields = ('title', 'address', 'area', 'city', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_owner_edit_at')
    inlines = [PropertyPhotoInline]

@admin.register(PropertyPhoto)
class PropertyPhotoAdmin(admin.ModelAdmin):
    list_display = ('property', 'caption', 'uploaded_at')

@admin.register(PropertyEditRequest)
class PropertyEditRequestAdmin(admin.ModelAdmin):
    list_display = ('property', 'requester', 'status', 'created_at', 'reviewed_by', 'reviewed_at')
    list_filter = ('status',)
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        for req in queryset.filter(status='pending'):
            req.status = 'approved'
            req.reviewed_by = request.user
            req.reviewed_at = timezone.now()
            req.save()
            prop = req.property
            prop.owner_can_edit = True
            prop.save(update_fields=['owner_can_edit'])

    def reject_requests(self, request, queryset):
        for req in queryset.filter(status='pending'):
            req.status = 'rejected'
            req.reviewed_by = request.user
            req.reviewed_at = timezone.now()
            req.save()

@admin.register(PropertyDeleteRequest)
class PropertyDeleteRequestAdmin(admin.ModelAdmin):
    list_display = ('property', 'requester', 'status', 'created_at', 'reviewed_by', 'reviewed_at')
    list_filter = ('status',)
    actions = ['approve_delete_requests', 'reject_delete_requests']

    def approve_delete_requests(self, request, queryset):
        for req in queryset.filter(status='pending'):
            req.status = 'approved'
            req.reviewed_by = request.user
            req.reviewed_at = timezone.now()
            req.save()
            if req.property:
                req.property.delete()

    def reject_delete_requests(self, request, queryset):
        for req in queryset.filter(status='pending'):
            req.status = 'rejected'
            req.reviewed_by = request.user
            req.reviewed_at = timezone.now()
            req.save()