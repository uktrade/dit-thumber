default_app_config = 'thumber.apps.ThumberConfig'


def _expose_items():
    from .decorators import thumber_feedback
    globals()['thumber_feedback'] = thumber_feedback
