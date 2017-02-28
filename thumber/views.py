import os
from urllib.parse import urlparse
from itertools import chain

from django.views.generic.edit import View
from django.core.urlresolvers import resolve
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed

from .models import ContentFeedback
from .forms import ContentFeedbackForm


__all__ = ['thumber_feedback']


def thumber_feedback(view):
    # Make a new class that inherits from the ContentFeedbackView, and the wrapped view class
    return type('ThumberFeedbackView', (ContentFeedbackView, view,), {})


class ContentFeedbackView():

        satisfired_wording = 'Was this service useful?'
        yes_wording = 'Yes, thanks'
        no_wording = 'Not really'
        comment_wording = ''
        comment_placeholder = 'Please tell us why?'
        submit_wording = 'Send my feedback'
        thanks_message = 'Thank you for your feedback'
        error_message = 'Sorry, something went wrong'
        first_option_yes = True

        def get(self, request, *args, **kwargs):
            # Need to set something in the session to ensure that the user gets a session cookie
            self.request.session['thumber'] = None
            return super().get(request, *args, **kwargs)

        def get_template_names(self):
            templates = []
            view_components = self.request.resolver_match.view_name.split(':')
            templates.append(os.path.join(*chain(['thumber'], view_components, ['feedback.html'])))
            if len(view_components) > 1:
                for ind in range(1, len(view_components)):
                    # arbitrary namespaces can be used with a view, so iterate over all options building up paths to
                    # possible templates
                    template = os.path.join(*chain(['thumber'], view_components[:-ind], ['feedback.html']))
                    templates.append(template)

            # Add in the standard thumber feedback template as the fallback if no custom templates are found
            templates.append(os.path.join('thumber', 'feedback.html'))

            return templates

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            names = super().get_template_names()
            context['template_name'] = names[0]

            if self.request.method == 'POST' and self.request.POST.get('thumber_token', None) == 'sync':
                # feedback has been given via non AJAX request, add the 'thank you' message to the context
                context['thanks_message'] = self.thanks_message
            else:
                options = {
                    'satisfied_wording': self.satisfired_wording,
                    'yes_wording': self.yes_wording,
                    'no_wording': self.no_wording,
                    'comment_wording': self.comment_wording,
                    'comment_placeholder': self.comment_placeholder,
                    'first_option_yes': self.first_option_yes
                }
                context['thumber_form'] = ContentFeedbackForm(**options)
                context.update(options)
                context['submit_wording'] = self.submit_wording
                context['thanks_message'] = self.thanks_message
                context['error_message'] = self.error_message

            return context

        def post(self, request, *args, **kwargs):
            if request.POST.get('thumber_token', None) is not None:
                pk = request.POST.get('id', None)
                if pk is None or pk == '':
                    # No PK, this means we need to create a new ContentFeedback object
                    http_referer = self.request.META.get('HTTP_REFERER')
                    sessionid = self.request.COOKIES[settings.SESSION_COOKIE_NAME]
                    user_feedback = ContentFeedbackForm(data=request.POST).save(commit=False)
                    user_feedback.url = http_referer
                    user_feedback.view_name = self._get_view_from_url(http_referer)
                    user_feedback.session = sessionid
                else:
                    # PK given, so this ContentFeedback already exists and just needs the comment adding
                    user_feedback = ContentFeedback.objects.get(pk=pk)
                    user_feedback.comment = request.POST['comment']

                user_feedback.save()

                if request.POST.get('thumber_token', None) == 'sync':
                    # Non-AJAX post, we've now done the processing, so return super's GET response
                    return self.get(request)
                else:
                    # AJAX submission, inform frontend the frontend the POST was successful, and give the id back so it
                    # can be updated in a separate request
                    return JsonResponse({"success": True, "id": user_feedback.id})
            else:
                try:
                    return super().post(request, *args, **kwargs)
                except AttributeError:
                    methods = [m.upper() for m in self.http_method_names if hasattr(self, m) and m.upper() != 'POST']
                    return HttpResponseNotAllowed(methods)

        def _get_view_from_url(self, url):
            url_data = urlparse(url)
            host = url_data.netloc
            path = url_data.path
            viewname = resolve(path).view_name
            return viewname
