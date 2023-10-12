from django.urls import re_path

from . import views

app_name = 'thumber_tests'


urlpatterns = [
    re_path(r'^example$', views.ExampleTemplateView.as_view(), name='example'),
    re_path(
        r'^multiexample$',
        views.ExampleMultipleTemplateView.as_view(),
        name='multiexample',
    ),
    re_path(
        r'^bad_example$', views.BadExampleTemplateView.as_view(), name='bad_example'
    ),
    re_path(
        r'^args_example/([\w]+)$', views.ArgsExampleView.as_view(), name='args_example'
    ),
    re_path(
        r'^kwargs_example/(?P<slug>[\w-]+)$',
        views.KwargsExampleView.as_view(),
        name='kwargs_example',
    ),
    re_path(r'^form$', views.ExampleFormView.as_view(), name='example_form'),
    re_path(
        r'^form_success$',
        views.ExampleFormSuccessView.as_view(),
        name='example_form_success',
    ),
    re_path(
        r'^override_template_example$',
        views.ExampleOverrideTemplateView.as_view(),
        name='override_template_example',
    ),
]
