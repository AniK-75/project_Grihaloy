from django.db import models

# Create your models here.
class HeatmapService(models.Model):
    heatmap_id = models.UUIDField(primary_key=True)
    area = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    intensity_score = models.FloatField()

    def __str__(self):
        return f"{self.area} - {self.service_type}"