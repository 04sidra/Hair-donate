from django.apps import AppConfig


class HairAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hair_app'
    
    def ready(self):
        import hair_app.signals