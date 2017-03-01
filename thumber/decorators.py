import types

from django.core.exceptions import ImproperlyConfigured
from django.views.generic import View

from .views import ContentFeedbackView


def thumber_feedback(view):
    # Cannot wrap view functions or classes that don't inherit from class-based View
    if type(view) is types.FunctionType or not issubclass(view, View):
        raise ImproperlyConfigured('Only class-based views can be decorated with `thumber_feedback')

    # Make a new class that inherits from the ContentFeedbackView, and the wrapped view class
    return type('ThumberFeedbackView', (ContentFeedbackView, view,), {})
