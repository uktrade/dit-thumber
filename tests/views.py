from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from thumber.decorators import thumber_feedback

from .forms import ExampleForm


@thumber_feedback
class ExampleTemplateView(TemplateView):
    def get_template_names(self):
        return ['example.html']

    def get_context_data(self, **kwargs):
        return {'example_key': 'example_val'}


@thumber_feedback
class ExampleMultipleTemplateView(TemplateView):
    def get_template_names(self):
        return ['non_existant.html', 'example.html']

    def get_context_data(self, **kwargs):
        return {'example_key': 'example_val'}


@thumber_feedback
class ArgsExampleView(TemplateView):
    template_name = 'example.html'

    def get(self, request, arg):
        return super().get(request)


@thumber_feedback
class KwargsExampleView(TemplateView):
    template_name = 'example.html'

    def get(self, request, slug=None):
        # ignore the slug keyword argument
        return super().get(request)


@thumber_feedback
class ExampleOverrideTemplateView(TemplateView):
    template_name = 'example.html'
    satisfied_wording = 'Did you find what you were looking for?'

    def get_submit_wording(self):
        return 'Send feedback!'


@thumber_feedback
class BadExampleTemplateView(TemplateView):
    template_name = 'bad_example.html'


@thumber_feedback
class ExampleFormView(FormView):
    template_name = 'example.html'
    form_class = ExampleForm
    success_url = reverse_lazy('thumber_tests:example_form_success')


class ExampleFormSuccessView(TemplateView):
    template_name = 'example.html'
