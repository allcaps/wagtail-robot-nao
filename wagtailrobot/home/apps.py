from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'home'
    verbose_name = "Home app"

    def ready(self):
        import signals  # noqa
