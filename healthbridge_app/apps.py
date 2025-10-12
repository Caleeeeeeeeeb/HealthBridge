from django.apps import AppConfig


class HealthbridgeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'healthbridge_app'

    def ready(self):
        """Import signals when Django starts"""
        import healthbridge_app.signals
