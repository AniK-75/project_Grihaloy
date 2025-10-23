from django.apps import AppConfig

class HeatmapServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'heatmap_service'

    def ready(self):
        import heatmap_service.signals
