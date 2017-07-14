==============
Django Thumber
==============

Department of International Trade Django Thumber.  A Django app to solicit user feedback on various views/pages via a
simple widget.

Includes it's own Javascript to handle showing/hiding parts of the form, and performing AJAX requests to the server,
but also works when Javascript is disabled/unavailable in the client browser.

The user interaction is kept to a minimum, but captured as part of the feedback includes metadata about the user's
session, the timestamp of the feedback, the name of view that the feedback was given about, and the full url of the
page.

Requirements
------------

* Python >= 3.4
* Django >= 1.9
* jQuery >= 1.7


===========
Quick start
===========

#. Install the package::

    $ pip install django-thumber

#. Add "thumber" to your INSTALLED_APPS setting::

    INSTALLED_APPS = [
        ...
        'thumber',
    ]

#. Run ``python manage.py migrate`` to create the thumber models.

#. Run ``python manage.py collectstatic`` to pull in the static files for thumber.

#. Ensure your base template (or other template that the view extends) defines an 'extra_js' block, which is *after* 
   the inclusion of jQuery::

    <script src="https://code.jquery.com/jquery-x.y.z.min.js></script>
    ...
    {% block extra_js %}{% endblock %}
    ...

#. Mark your class-based view with the decorator provided by thumber::

    from thumber.decorators import thumber_feedback

    @thumber_feedback
    class MyView(...):
        ...

#. Ensure the template for your view (or another template that the view extends) defines a 'thumber_feedback' block
   where you want the widget to appear on the page::

    {% block thumber_feedback %}{% endblock %}


================
Getting Data Out
================

It is recommended that you register the ContentFeedback model to the admin interface (if you are using it in your project),
so you can easily go through it's data and can specify the fields you want to see, something like::
    
    from django.contrib import admin
    from thumber.models import ContentFeedback

    @admin.register(ContentFeedback)
    class ContentFeedbackAdmin(admin.ModelAdmin):

        list_display = ['created', 'satisfied', 'view_name', 'comment']
        ordering = ['created']

And of course you can always just inspect the models directly in code or the django shell::

    from thumber.models import ContentFeedback
    ContentFeedback.objects.all()
    ...

There is one simple shortcut which is a common use case, to see the average feedback for each view in your applcation.
To get aggregate data for every view, there is a shortcut on the model manager of the ContentFeedbcak model::
    
    from thumber.models import ContentFeedback
    ContentFeedback.objects.average_for_views()
    [ ... ]

Or it can be performed on queryset too, meaning you can prefilter (e.g. to date ranges) before aggregating::
    
    from datetime import datetime, timedelta
    from thumber.models import ContentFeedback
    
    # Get data only for the past week
    ContentFeedback.objects.filter(created__gt=datetime.now() - timedelta(days=7)).average_for_views()
    [ ... ]

=====================
Further configuration
=====================

You can add properties to you view class to modify various properties of the widget, shown below are the default values,
just set the replacements as needed on your view class::

    @thumber_feedback
    class MyView(...):
        satisfied_wording = "Was this service useful?"  # The initial question presented to the user
        yes_wording = "Yes, thanks"                     # The positive radio option wording
        no_wording = "Not really"                       # The negative radio option wording
        comment_wording = ""                            # The label wording for the comment textarea
        comment_placeholder = "Please tell us why?"     # The placeholder text for the comment textares
        submit_wording = "Send my feedback"             # The text on the submit button
        thanks_message = "Thank you for your feedback"  # The success/thank you message wording
        error_message = "Sorry, something went wrong"   # The failure message
        first_option_yes = True                         # Whether "Yes, thanks" appears as the first radio option

Any of the above properties can also be added as methods with the prefix ``get_``, and such methods will take preference over
a variable::

    @thumber_feedback
    class MyView(...):

        def get_satisfied_wording(self):
            return "Did you find this page about {0} useful?".format(self.page_description)


You can hook into the success and error processing of the thumber to perform custom actions when sending feedback.  To
do so, after the ``extra_js`` block in your template, there will be a ``thumber`` Javascript variable available.  You
can set custom handlers like so::

    thumber.setSuccessHandler(alert('Yay!'));
    thumber.setErrorHandler(alert('Boo!'));

You can override the template used to render the widget, by creating your own template.  This must be named
feedback.html, and be in a 'thumber' directory within your templates.

Further, the template can be overridden on a project, app, or view level, based upon where the template is located.  In
order of preference, thumber will look for templates in the following locations::

    thumber/YOUR_APP/YOUR_VIEW_NAME/feedback.html  # Override for the specific YOUR_VIEW_NAME view
    thumber/YOUR_APP/feedback.html                 # Override for all views in YOUR_APP
    thumber/feedback.html                          # Override for all views in all apps of your project

Some guidance on how to write a custom feedback.html template is below

Overriding in feedback.html
---------------------------

If you create a custom feedback.html template you have a number of blocks you can override, some give more flexibility,
but come with extra reponsibility to ensure you perform certain work yourself.

Blocks to override, and some simlpe guidance for each are as follows:

* ``thumber_form_class``
    * Add addtional class/classes to the thumber form
* ``before_thumber_form`` and ``after_thumber_form``
    * The blocks are directly either side of the <form></form> tags
    * Use to wrap the form with html if necesssary
* ``thumber_form_widgets``
    * This replaces just the widgets inside the form, including the submit button, these must be replaced
    * A variable of ``thumber_form`` is available which you can use to render the controls
    * If you do not use the thumber_form, the minimum needed data in the post is:
        * satisfied, as a radio button with values "True" or "False"
        * comment, as textarea
        * thumber_token (hidden input), as "sync" for non-Javascript posts, or "ajax" for Javascript posts
        * All inputs require an id
    * The form tag, including csrf token are handled, and do not need including
* ``thumber_form``
    * This replaces the entire form, so it will need redefining
    * The form **must** have a 'thumber-form' class for the ajax code to work
    * The form's action must be the url of the view that is decorated with @thumber_view


============
Contributing
============

Contributions are welcome. Please follow the guidelines below to make life easier:

* Fork the repo, branch off release, make changes, then make a pull request (PR) to release on the main repo
* Include tests for bug fixes or new features
* Include documentation for any new features
* Please limit changes for a PR to a single feature, or a single bugfix
    * Make multiple PRs for multiple discrete changes
* Please squash commits - ideally a single commit, but at least to a sensible minimum
    * If a PR reasonably should have multiple commits, consider if it should *actually* be separate PRs


=======
License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/uktrade/dit-thumber/blob/master/LICENSE>`_ file for more
details.
