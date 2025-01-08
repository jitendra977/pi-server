from django.apps import AppConfig
from server.app_helper.signals import setup_signal_handlers



class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server'

    def ready(self):
        setup_signal_handlers()
