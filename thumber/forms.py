from django import forms
from django.core.urlresolvers import resolve

from .models import ContentFeedback


class ContentFeedbackForm(forms.ModelForm):

    class Meta:
        model = ContentFeedback
        fields = ['satisfied', 'comment']

    thumber_token = forms.CharField(initial='sync', widget=forms.HiddenInput())
    satisfied = forms.TypedChoiceField(
                    coerce=lambda val: val == 'True',
                    choices=((True, 'Yes'), (False, 'No')),
                    widget=forms.RadioSelect
                )

    def __init__(self, **kwargs):
        """
        The view may pass in some wording changes for the form.
        They will be passed in from the view, since this is outward interface for developers
        """

        satisfied_wording = kwargs.pop('satisfied_wording', None)
        yes_wording = kwargs.pop('yes_wording', None)
        no_wording = kwargs.pop('no_wording', None)
        comment_wording = kwargs.pop('comment_wording', None)
        comment_placeholder = kwargs.pop('comment_placeholder', None)
        true_first = kwargs.pop('first_option_yes', True)

        super().__init__(**kwargs)

        if satisfied_wording is not None:
            self.fields['satisfied'].label = satisfied_wording
        if yes_wording is not None:
            choices = self.fields['satisfied'].choices
            new_choices = [(True, yes_wording), choices[1]]
            self.fields['satisfied'].choices = new_choices
        if no_wording is not None:
            choices = self.fields['satisfied'].choices
            new_choices = [choices[0], (False, no_wording)]
            self.fields['satisfied'].choices = new_choices
        if comment_wording is not None:
            self.fields['comment'].label = comment_wording
        if comment_placeholder is not None:
            self.fields['comment'].widget.attrs['placeholder'] = comment_placeholder

        if not true_first:
            choices = self.fields['satisfied'].choices
            self.fields['satisfied'].choices = (choices[1], choices[0])
