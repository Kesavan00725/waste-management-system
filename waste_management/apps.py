from django.apps import AppConfig

class WasteManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'waste_management'

    def ready(self):
        """Connect to MongoDB when the app is ready."""
        import mongoengine
        from django.conf import settings
        mongoengine.connect(
            db=settings.MONGODB_SETTINGS['db'],
            host=settings.MONGODB_SETTINGS['host'],
            port=settings.MONGODB_SETTINGS['port'],
        )
