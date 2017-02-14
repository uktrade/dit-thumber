from __future__ import unicode_literals

from django.db import models


class ContentFeedback(models.Model):
    """
    Basic model for storing user-submitted feedback audit data
    """

    created = models.DateTimeField(auto_now=True)
    satisfied = models.BooleanField()
    comment = models.TextField(null=True, blank=True)

    url = models.URLField()
    view_name = models.CharField(max_length=255)
    utm_params = models.TextField(null=True)
    session = models.CharField(max_length=64)

    def __str__(self):
        tick_cross = '✓' if self.satisfied else '✘'
        return "{0} - {1}".format(tick_cross, self.created)

    class Meta:
        ordering = ('-created',)
