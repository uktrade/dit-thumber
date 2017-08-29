from django.conf.urls import url

from . import views


app_name = 'thumber_tests'


urlpatterns = [
    url(r'^example$', views.ExampleTemplateView.as_view(), name='example'),
    url(r'^multiexample$', views.ExampleMultipleTemplateView.as_view(), name='multiexample'),
    url(r'^bad_example$', views.BadExampleTemplateView.as_view(), name='bad_example'),
    url(r'^args_example/([\w]+)$', views.ArgsExampleView.as_view(), name='args_example'),
    url(r'^kwargs_example/(?P<slug>[\w-]+)$', views.KwargsExampleView.as_view(), name='kwargs_example'),
    url(r'^form$', views.ExampleFormView.as_view(), name='example_form'),
    url(r'^form_success$', views.ExampleFormSuccessView.as_view(), name='example_form_success'),
    url(r'^override_template_example$', views.ExampleOverrideTemplateView.as_view(), name='override_template_example')
]
