from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from thumber.models import ContentFeedback
from thumber.decorators import thumber_feedback


class ThumberTests(TestCase):

    def test_bad_template_no_form(self):
        # Use a view whose template doesn't specify the thumber_feedback block
        response = self.client.get(reverse('thumber_tests:bad_example'))
        # Ensure it has it's regular content, but not the thumber form
        self.assertContains(response, 'Bad Example Template!', status_code=200)
        self.assertNotContains(response, 'Was this service useful?')

    def test_get_has_thumber_form(self):
        # Use a view whose template does correctly specify the thumber_feedback block
        response = self.client.get(reverse('thumber_tests:example'))
        # Ensure it has it's regular content and the thumber form
        self.assertContains(response, 'Example Template!', status_code=200)
        self.assertContains(response, 'Was this service useful?')

        # Check the context to make sure it has both the thumber_form, and what the view would normally add
        self.assertIn('thumber_form', response.context)
        self.assertEquals(response.context['example_key'], 'example_val')

    def test_original_post_method(self):
        # Use a form view and post it's normal form back to it to make sure the thumber post handling is ignored
        data = {'char_field': 'foo'}
        response = self.client.post(reverse('thumber_tests:example_form'), data)
        self.assertRedirects(response, reverse('thumber_tests:example_form_success'))

    def test_no_original_post_method(self):
        # Use a view with no post method, and make sure that if the thumber form is not posted, we get a 400
        response = self.client.post(reverse('thumber_tests:example'), {})
        self.assertEquals(response.status_code, 405)

    def test_non_js_post_workflow(self):
        """ Post to a view ensuring that the response is like the normal 'get' response, but with
        the thumber success message, and that a populated ContentFeedback model is created.
        """

        view_name = 'thumber_tests:example_form'
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
        view_name = 'thumber_tests:example_form'
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

    def test_view_with_kwargs(self):
        """Dedicated test to ensure that views with kwargs still work
        """
        view_name = 'thumber_tests:kwargs_example'
        path = reverse(view_name, kwargs={'slug': 'foobar'})
        response = self.client.get(path)
        self.assertContains(response, 'Example Template!', status_code=200)
        self.assertContains(response, 'Was this service useful?')

    def test_basic_template_override(self):
        # Check that the example views (the good ones) correctly get the app-level feedback.html overrides
        response = self.client.get(reverse('thumber_tests:example'))
        self.assertContains(response, 'test before form', status_code=200)
        self.assertContains(response, 'test after form')

        response = self.client.get(reverse('thumber_tests:example_form'))
        self.assertContains(response, 'test before form', status_code=200)
        self.assertContains(response, 'test after form')

    def test_complex_template_override(self):
        response = self.client.get(reverse('thumber_tests:override_template_example'))
        self.assertContains(response, 'new test before form', status_code=200)
        self.assertContains(response, 'Did you find what you were looking for?')
        self.assertContains(response, 'Send feedback!')
        self.assertNotContains(response, 'test after form')
        self.assertContains(response, '<input type="reset" value="reset" />')

    def test_cannot_decorate_view_function(self):
        """Attempt to decorate a view function, check that ImproperlyConfigured gets raised,
        as it can only be used to decorate django class-based views
        """
        with self.assertRaises(ImproperlyConfigured):
            @thumber_feedback
            def view_function(request):
                return None

    def test_cannot_decorate_non_class_views(self):
        """Attempt to decorate a class that does not inherit django.views.generic.View,
        ImproperlyConfigured should get raised, as it can only be used to decorate django class-based views
        """
        with self.assertRaises(ImproperlyConfigured):
            @thumber_feedback
            class NonClassView():
                pass


class ThumberAggregationTests(TestCase):

    def test_simple_view_averages(self):
        """ Submit a mix of feedback to a view, and then ask the model manager for average feedback
        """

        view_name = 'thumber_tests:example'
        path = reverse(view_name)
        http_referer = 'http://example.com{0}'.format(path)

        # Get the form view, and 'follow' so that the session cookie gets set on the client
        response = self.client.get(path, follow=True)

        # Post with thumber_token=ajax for a JSON response
        data = {'satisfied': 'False', 'thumber_token': 'ajax'}
        self.client.post(path, data, HTTP_REFERER=http_referer)

        # Post again with positive feedback, a few times
        data = {'satisfied': 'True', 'thumber_token': 'ajax'}
        self.client.post(path, data, HTTP_REFERER=http_referer)
        self.client.post(path, data, HTTP_REFERER=http_referer)
        self.client.post(path, data, HTTP_REFERER=http_referer)

        # Check we have 4 feedbacks
        feedback = ContentFeedback.objects.count()
        self.assertEquals(feedback, 4)

        # Get the average of feedbacks
        average_feedback = ContentFeedback.objects.average_for_views()

        # There should only be one item, as it's grouped on view name
        self.assertEquals(len(average_feedback), 1)

        # And the one item should have keys 'avg' and 'view_name'
        self.assertEquals(len(average_feedback[0]), 2)
        self.assertIn('avg', average_feedback[0])
        self.assertIn('view_name', average_feedback[0])

        # The view name should be our app's example_view, and the average should be 75% positive
        self.assertEquals(average_feedback[0]['view_name'], view_name)
        self.assertEquals(average_feedback[0]['avg'], 0.75)

        # We can also get the average feedback per view on a queryset (equivalent to above)
        average_feedback = ContentFeedback.objects.all().average_for_views()
        self.assertEquals(average_feedback[0]['view_name'], view_name)
        self.assertEquals(average_feedback[0]['avg'], 0.75)

    def test_view_averages_filtered(self):
        """ Submit feedback to multiple views, and make sure that we can filter the queryset
        and still get easy aggregated feedback data
        """

        view_name1 = 'thumber_tests:example'
        view_name2 = 'thumber_tests:example_form'

        path1 = reverse(view_name1)
        http_referer1 = 'http://example.com{0}'.format(path1)

        path2 = reverse(view_name2)
        http_referer2 = 'http://example.com{0}'.format(path2)

        # Get the form view, and 'follow' so that the session cookie gets set on the client
        self.client.get(path1, follow=True)
        data = {'satisfied': 'False', 'thumber_token': 'ajax'}
        self.client.post(path1, data, HTTP_REFERER=http_referer1)
        data = {'satisfied': 'True', 'thumber_token': 'ajax'}
        self.client.post(path1, data, HTTP_REFERER=http_referer1)

        # Then add some feedback on the other view
        self.client.get(path2, follow=True)
        data = {'satisfied': 'True', 'thumber_token': 'ajax'}
        self.client.post(path2, data, HTTP_REFERER=http_referer2)

        # Check we have 3 feedbacks
        feedback = ContentFeedback.objects.count()
        self.assertEquals(feedback, 3)

        # Get the average of feedbacks
        average_feedback = ContentFeedback.objects.average_for_views()

        # There should only be 2 item, one for each view
        self.assertEquals(len(average_feedback), 2)

        # Get the average of feedbacks for the first view
        average_feedback1 = ContentFeedback.objects.filter(view_name=view_name1).average_for_views()

        # The view name should be our app's example_view, and the average should be 50% positive
        self.assertEquals(average_feedback1[0]['view_name'], view_name1)
        self.assertEquals(average_feedback1[0]['avg'], 0.5)

        # Get the average of feedbacks for the second view
        average_feedback2 = ContentFeedback.objects.filter(view_name=view_name2).average_for_views()

        # The view name should be our app's example_view, and the average should be 100% positive
        self.assertEquals(average_feedback2[0]['view_name'], view_name2)
        self.assertEquals(average_feedback2[0]['avg'], 1.0)
