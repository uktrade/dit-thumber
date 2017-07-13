from __future__ import unicode_literals

from django.db import models
from django.db.models import Avg, Case, When, Value, IntegerField


class FeedbackQuerySet(models.QuerySet):

    def average_for_views(self):
        case = Case(When(satisfied=True, then=Value(1)),
                    When(satisfied=False, then=Value(0)),
                    output_field=IntegerField())

        return self.values('view_name').annotate(avg=Avg(case)).order_by('view_name')


class FeedbackManager(models.Manager):

    def get_queryset(self):
        return FeedbackQuerySet(self.model, using=self._db)

    def average_for_views(self):
        return self.get_queryset().average_for_views()


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

    objects = FeedbackManager()

    def __str__(self):
        tick_cross = '✓' if self.satisfied else '✘'
        return "{0} - {1}".format(tick_cross, self.created)

    class Meta:
        ordering = ('-created',)
