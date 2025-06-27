from django.apps import AppConfig


class AppFaunaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_fauna"


def ready(self):
    import app_fauna.signals
