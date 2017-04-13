from django import forms


class ExampleForm(forms.Form):
    char_field = forms.CharField()
