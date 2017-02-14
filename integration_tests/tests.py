from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from thumber.models import ContentFeedback


class ThumberTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_bad_template_no_form(self):
        # Use a view whose template doesn't specify the thumber_feedback block
        response = self.client.get(reverse('thumber_integration_tests:bad_example'))
        # Ensure it has it's regular content, but not the thumber form
        self.assertContains(response, 'Bad Example Template!', status_code=200)
        self.assertNotContains(response, 'Was this service useful?')

    def test_get_has_thumber_form(self):
        # Use a view whose template does correctly specify the thumber_feedback block
        response = self.client.get(reverse('thumber_integration_tests:example'))
        # Ensure it has it's regular content and the thumber form
        self.assertContains(response, 'Example Template!', status_code=200)
        self.assertContains(response, 'Was this service useful?')

        # Check the context to make sure it has both the thumber_form, and what the view would normally add
        self.assertIn('thumber_form', response.context)
        self.assertEquals(response.context['example_key'], 'example_val')

    def test_original_post_method(self):
        # Use a form view and post it's normal form back to it to make sure the thumber post handling is ignored
        data = {'char_field': 'foo'}
        response = self.client.post(reverse('thumber_integration_tests:example_form'), data)
        self.assertRedirects(response, reverse('thumber_integration_tests:example_form_success'))

    def test_no_original_post_method(self):
        # Use a view with no post method, and make sure that if the thumber form is not posted, we get a 400
        response = self.client.post(reverse('thumber_integration_tests:example'), {})
        self.assertEquals(response.status_code, 405)

    def test_non_js_post_workflow(self):
        """ Post to a view ensuring that the response is like the normal 'get' response, but with
        the thumber success message, and that a populated ContentFeedback model is created.
        """

        view_name = 'thumber_integration_tests:example_form'
        path = reverse(view_name)
        http_referer = 'http://example.com{0}'.format(path)

        # Get the form view, and 'follow' so that the session cookie gets set on the client
        response = self.client.get(path, follow=True)
        self.assertIn(settings.SESSION_COOKIE_NAME, response.cookies)

        # Post the thumber form, and get the same page but with teh success message
        data = {'satisfied': 'True', 'comment': 'test comment', 'thumber_token': 'sync'}
        response = self.client.post(path, data, HTTP_REFERER=http_referer)
        self.assertContains(response, 'Thank you for your feedback', status_code=200)

        # Check that a ContentFeedback model was created with the correct details
        self.assertEquals(ContentFeedback.objects.count(), 1)
        feedback = ContentFeedback.objects.all()[0]
        self.assertEquals(feedback.view_name, view_name)
        self.assertEquals(feedback.url, http_referer)
        self.assertEquals(feedback.satisfied, True)
        self.assertEquals(feedback.comment, 'test comment')

    def test_overriden_ajax_post(self):
        view_name = 'thumber_integration_tests:example_form'
        path = reverse(view_name)
        http_referer = 'http://example.com{0}'.format(path)

        # Get the form view, and 'follow' so that the session cookie gets set on the client
        response = self.client.get(path, follow=True)
        self.assertIn(settings.SESSION_COOKIE_NAME, response.cookies)

        # Post with thumber_token=ajax for a JSON response
        data = {'satisfied': 'False', 'thumber_token': 'ajax'}
        response = self.client.post(path, data, HTTP_REFERER=http_referer)
        self.assertEquals(response['Content-Type'], 'application/json')

        # Check we got a success message in our json
        json = response.json()
        self.assertIn('success', json)
        self.assertEquals(json['success'], True)
        pk = json['id']

        self.assertEquals(ContentFeedback.objects.count(), 1)
        feedback = ContentFeedback.objects.all()[0]
        self.assertEquals(feedback.view_name, view_name)
        self.assertEquals(feedback.url, http_referer)
        self.assertEquals(feedback.satisfied, False)

        # Resbumit now with the ID, and set the comment
        data = {'thumber_token': 'ajax', 'id': pk, 'comment': 'test comment'}
        response = self.client.post(path, data, HTTP_REFERER=http_referer)
        self.assertEquals(response['Content-Type'], 'application/json')

        json = response.json()
        self.assertIn('success', json)
        self.assertEquals(json['success'], True)
        # There should still only be 1 model, and it shoudl now have the test comment
        self.assertEquals(ContentFeedback.objects.count(), 1)
        feedback = ContentFeedback.objects.all()[0]
        self.assertEquals(feedback.comment, 'test comment')

    def test_basic_template_override(self):
        # Check that the example views (the good ones) correctly get the app-level feedback.html overrides
        response = self.client.get(reverse('thumber_integration_tests:example'))
        self.assertContains(response, 'test before form', status_code=200)
        self.assertContains(response, 'test after form')

        response = self.client.get(reverse('thumber_integration_tests:example_form'))
        self.assertContains(response, 'test before form', status_code=200)
        self.assertContains(response, 'test after form')

    def test_complex_template_override(self):
        response = self.client.get(reverse('thumber_integration_tests:override_template_example'))
        self.assertContains(response, 'new test before form', status_code=200)
        self.assertNotContains(response, 'test after form')
        self.assertContains(response, '<input type="reset" value="reset" />')
