from django.apps import AppConfig


class TestConfig(AppConfig):
    name = 'tests'

    def ready(self):
        return super().ready()
