from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['created', 'satisfied', 'view_name', 'comment']
    ordering = ['created']


if not admin.site.is_registered(Feedback):
    admin.site.register(Feedback, FeedbackAdmin)
