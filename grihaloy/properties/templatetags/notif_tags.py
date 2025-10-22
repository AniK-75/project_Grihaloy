from django import template
from properties.models import PropertyEditRequest, PropertyDeleteRequest

register = template.Library()

@register.simple_tag(takes_context=True)
def notification_count(context):
    """
    Returns number of reviewed outcomes (approved/rejected) for the current user.
    Pending requests are NOT counted.
    Works for both LANDLORD and RENTER.
    """
    request = context.get('request')
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return 0

    edit_count = PropertyEditRequest.objects.filter(
        requester=user, status__in=['approved', 'rejected']
    ).count()

    del_count = PropertyDeleteRequest.objects.filter(
        requester=user, status__in=['approved', 'rejected']
    ).count()

    return edit_count + del_count