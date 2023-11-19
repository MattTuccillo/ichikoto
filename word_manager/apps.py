from django.apps import AppConfig
from .services.scheduler_service import start_background_task
import threading


class WordManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'word_manager'

    def ready(self):
        if threading.current_thread() == threading.main_thread():
            start_background_task()
