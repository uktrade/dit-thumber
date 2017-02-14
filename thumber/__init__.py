default_app_config = 'thumber.apps.ThumberConfig'


def _expose_items():
    from .views import thumber_feedback
    globals()['thumber_feedback'] = thumber_feedback
