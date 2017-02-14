from django.apps import AppConfig
from . import _expose_items


class ThumberConfig(AppConfig):
    name = 'thumber'

    def ready(self):
        _expose_items()
