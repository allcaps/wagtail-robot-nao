from django.template.defaultfilters import slugify
from django.views.generic import FormView
from django.views.generic import TemplateView

from forms import StartForm
from django.contrib.auth.models import User


class StartView(FormView):
    form_class = StartForm
    template_name = "home/start.html"
    success_url = "/credentials/"

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        username = slugify(name).replace('-', '')

        self.request.session['name'] = name
        self.request.session['username'] = username

        User.objects.create_user(
            username,
            '',  # No email.
            '1234',
            is_staff=True,
            first_name=name,
        )
        return super(StartView, self).form_valid(form)


class CredentialView(TemplateView):
    template_name = "home/credentials.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(CredentialView, self).get_context_data(*args, **kwargs)
        ctx['username'] = self.request.session.get('username')
