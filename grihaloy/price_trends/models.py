from django.db import models

# Create your models here.
class PriceTrend(models.Model):
    trend_id = models.UUIDField(primary_key=True)
    area = models.CharField(max_length=100)
    avg_price = models.DecimalField(max_digits=10, decimal_places=2)
    popularity_score = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.area} - {self.avg_price}"