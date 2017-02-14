from django.conf.urls import url, include
from .views import ExampleTemplateView


urlpatterns = [
    url(r'^', include('integration_tests.urls')),
]
