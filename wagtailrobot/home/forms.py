from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout
from django import forms


class StartForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="What is your name?",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
