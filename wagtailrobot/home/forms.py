from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout
from django import forms


class StartForm(forms.Form):
    name = forms.CharField(max_length=255, label="Your name")

    def __init__(self, *args, **kwargs):
        super(StartForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name'),
            Div(
                StrictButton(
                    'Start',
                    css_class='submit-widget button-field btn btn-primary',
                    type='submit'
                ),
                css_class='formControls'
            ),
        )
