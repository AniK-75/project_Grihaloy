from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    RENTER = 'RENTER'
    LANDLORD = 'LANDLORD'
    ADMIN = 'ADMIN'
    ROLE_CHOICES = [
        (RENTER, 'Renter'),
        (LANDLORD, 'Landlord'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=RENTER)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='images/default.png')
    is_approved = models.BooleanField(default=False, help_text='Set to true when the user is approved by an admin.')

    # --- NEW FIELD FOR THE VERIFIED BADGE ---
    is_kyc_verified = models.BooleanField(default=False,
                                          help_text='Set to true when a user has an approved KYC document.')

    def __str__(self):
        return f"{self.username} ({self.role})"


class VerificationDocument(models.Model):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verification_docs')
    doc = models.FileField(upload_to='verification_docs/')
    doc_type = models.CharField(max_length=120, blank=True, help_text="e.g., NID, Passport")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Doc {self.pk} for {self.user.username} - {self.status}"


class Rating(models.Model):
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_ratings')
    rated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_ratings')
    score = models.PositiveSmallIntegerField(default=5)  # 1-5
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.score} by {self.rater.username} for {self.rated.username}"