from django import template
from properties.models import Negotiation
from django.db.models import Q

register = template.Library()


@register.simple_tag(takes_context=True)
def negotiation_notification_count(context, user):
    if not user.is_authenticated:
        return 0

    unseen_count = 0
    if user.role == 'RENTER':
        unseen_count = Negotiation.objects.filter(
            renter=user,
            is_active=True,
            seen_by_renter=False
        ).count()
    elif user.role == 'LANDLORD':
        unseen_count = Negotiation.objects.filter(
            landlord=user,
            is_active=True,
            seen_by_landlord=False
        ).count()
    return unseen_count


@register.simple_tag(takes_context=True)
def notification_count(context):
    """
    Returns the total notification count for the logged-in user,
    including property edit/delete requests ONLY.
    Negotiation messages are handled by 'negotiation_notification_count'.
    """
    user = context['request'].user
    if not user.is_authenticated:
        return 0

    total_count = 0

    # Existing notification logic (edit/delete requests)
    if user.role == 'RENTER' or user.role == 'LANDLORD':
        from properties.models import PropertyEditRequest, PropertyDeleteRequest
        total_count += PropertyEditRequest.objects.filter(
            requester=user,
            status__in=['approved', 'rejected'],
            seen_by_requester=False
        ).count()
        total_count += PropertyDeleteRequest.objects.filter(
            requester=user,
            status__in=['approved', 'rejected'],
            seen_by_requester=False
        ).count()

    # --- FIX: REMOVED the line below that was double-counting ---
    # total_count += negotiation_notification_count(context, user)

    return total_count