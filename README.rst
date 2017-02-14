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

* Python >= 3.0
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

    from thumber import thumber_feedback

    @thumber_feedback
    class MyView(...):
        ...

#. Ensure the template for your view (or another template that the view extends) defines a 'thumber_feedback' block
   where you want the widget to appear on the page::

    {% block thumber_feedback %}{% endblock %}


=====================
Further configuration
=====================

You can add properties to you view class to modify various properties of the widget, shown below are the default values,
just set the replacements as needed on your view class::

    class MyView(ContentFeedbackMixin, ...):
        satisfired_wording = "Was this service useful?" # The initial question presented to the user
        yes_wording = "Yes, thanks"                     # The positive radio option wording
        no_wording = "Not really"                       # The negative radio option wording
        comment_wording = ""                            # The label wording for the comment textarea
        comment_placeholder = "Please tell us why?"     # The placeholder text for the comment textares
        submit_wording = "Send my feedback"             # The text on the submit button
        thanks_message = "Thank you for your feedback"  # The success/thank you message wording
        error_message = "Sorry, something went wrong"   # The failure message
        first_option_yes = True                         # Whether "Yes, thanks" appears as the first radio option

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

* Fork the repo, branch of master, make changes, then make a PR to the main repo
* Include tests for bug fixes or new features
* Include documentation for any new features
* Please limit changes for a PR to single-feature or single-bugfix changes - make multiple PRs for multiple discreet changes
* Please squash commits - ideally a single commit, but at least to a sensible minimum.


=======
License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/uktrade/dit-thumber/blob/master/LICENSE>`_ file for more
details.


====
TODO
====

* Get continuous integration to run on multiple python versions from 3.0+ 
    * Currently only running on 3.5.0
    * Utilise parallelism
* Run tests on multiple Django versions
    * Currently only running against Django 1.9
    * Utilise parallelism
