from django.db.models.signals import post_save
from django.dispatch import receiver
from properties.models import Property
from .models import AreaHeatmap


@receiver(post_save, sender=Property)
def update_heatmap_on_property_save(sender, instance, **kwargs):
    area = instance.area.strip().title()
    # Calculate new average price for that area
    properties_in_area = Property.objects.filter(area=area)
    prices = [float(p.price) for p in properties_in_area if p.price]
    avg_price = sum(prices) / len(prices) if prices else 0

    # Update or create heatmap entry
    heatmap, created = AreaHeatmap.objects.get_or_create(area=area)
    heatmap.avg_price = avg_price
    heatmap.update_color()
