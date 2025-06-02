from django.apps import AppConfig


class HomeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Home_App'


    def ready(self):
        import Home_App.signals



