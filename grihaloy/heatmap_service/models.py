from django.db import models

class AreaHeatmap(models.Model):
    area = models.CharField(max_length=100, unique=True)
    avg_price = models.FloatField(default=0)
    color = models.CharField(max_length=20, default="#31a354")  # green default

    def __str__(self):
        return f"{self.area} - {self.avg_price}"

    def update_color(self):
        """Assign color based on price range."""
        if self.avg_price > 22000000:
            self.color = "#e31a1c"  # red
        elif self.avg_price > 15000000:
            self.color = "#fd8d3c"  # orange
        elif self.avg_price > 10000000:
            self.color = "#fecc5c"  # yellow
        else:
            self.color = "#31a354"  # green
        self.save()
