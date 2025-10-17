from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AccountApprovalRequest

User = get_user_model()

@receiver(post_save, sender=User)
def create_account_approval_on_registration(sender, instance, created, **kwargs):
    if not created:
        return
    role = getattr(instance, 'role', None)
    is_approved = getattr(instance, 'is_approved', True)
    if role in ('RENTER', 'LANDLORD') and not is_approved:
        if not AccountApprovalRequest.objects.filter(user=instance, status='pending').exists():
            AccountApprovalRequest.objects.create(
                user=instance,
                reason=f'New {role.title()} registration awaiting approval.'
            )