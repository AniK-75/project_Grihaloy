from django.conf import settings
from django.db import models
import uuid

PROPERTY_TYPE_CHOICES = [
    ('apartment', 'Apartment'),
    ('room', 'Room'),
    ('sublet', 'Sublet'),
    ('house', 'House'),
    ('commercial', 'Commercial'),
]


class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')

    title = models.CharField(max_length=150, help_text='e.g., 2 Bed in Dhanmondi')
    description = models.TextField(blank=True)

    address = models.CharField(max_length=255)
    area = models.CharField(max_length=100, help_text='e.g., Dhanmondi, Uttara, Agrabad')
    city = models.CharField(max_length=50, default='Dhaka')

    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='apartment')
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    size_sqft = models.PositiveIntegerField(default=0)

    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_price_fixed = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    owner_can_edit = models.BooleanField(default=False)
    last_owner_edit_at = models.DateTimeField(null=True, blank=True)

    negotiable = models.BooleanField(default=False, help_text="Allow renters to negotiate price via chat.")  # NEW

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['area']),
            models.Index(fields=['city']),
            models.Index(fields=['price']),
            models.Index(fields=['is_active']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.area}, {self.city}'


class PropertyPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='property_photos/%Y/%m/%d/')
    caption = models.CharField(max_length=120, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Photo of {self.property.title}'


EDIT_STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class PropertyEditRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='edit_requests')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='property_edit_requests')
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=EDIT_STATUS, default='pending')
    admin_note = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='property_edit_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    # NEW: mark whether requester saw the outcome
    seen_by_requester = models.BooleanField(default=False, help_text="Requester has seen the final decision.")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'EditRequest({self.property.title}) by {self.requester} [{self.status}]'


class PropertyDeleteRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='delete_requests')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='property_delete_requests')
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=EDIT_STATUS, default='pending')
    admin_note = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='property_delete_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    # NEW: mark whether requester saw the outcome
    seen_by_requester = models.BooleanField(default=False, help_text="Requester has seen the final decision.")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'DeleteRequest({self.property and self.property.title}) by {self.requester} [{self.status}]'


# NEW MODELS FOR NEGOTIATION
class Negotiation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='negotiations')
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='started_negotiations')
    landlord = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='received_negotiations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Is this negotiation still open?")

    # NEW: Notification tracking
    seen_by_landlord = models.BooleanField(default=False, help_text="Landlord has seen the latest message.")
    seen_by_renter = models.BooleanField(default=False, help_text="Renter has seen the latest message.")

    class Meta:
        unique_together = ('property', 'renter')  # A renter can only have one negotiation per property
        ordering = ['-updated_at']

    def __str__(self):
        return f"Negotiation for {self.property.title} between {self.renter.username} and {self.landlord.username}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negotiation = models.ForeignKey(Negotiation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, help_text="The time the message was originally created.")

    # --- START MODIFIED BLOCK ---
    updated_at = models.DateTimeField(auto_now=True, help_text="The time the message was last edited.")
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # --- END MODIFIED BLOCK ---

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} in {self.negotiation}"