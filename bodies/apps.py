from django.apps import AppConfig


class BodiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bodies'
    
    def ready(self):
        import bodies.signals
