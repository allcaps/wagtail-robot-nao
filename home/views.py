from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.views.generic import FormView, TemplateView
from forms import StartForm


class StartView(FormView):
    form_class = StartForm
    template_name = "home/start.html"
    success_url = "/credentials/"

    def get(self, *args, **kwargs):
        """Remove all sessions before we start."""
        for key in self.request.session.keys():
            del self.request.session[key]
        return super(StartView, self).get(*args, **kwargs)

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        username = slugify(name).replace('-', '')

        self.request.session['name'] = name
        self.request.session['username'] = username

        User.objects.create_user(
            username,
            '',  # No email.
            '1234',
            first_name=name,
            is_staff=True,
            is_superuser=True,
        )
        return super(StartView, self).form_valid(form)


class CredentialView(TemplateView):
    template_name = "home/credentials.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(CredentialView, self).get_context_data(*args, **kwargs)
        ctx['username'] = self.request.session.get('username')
        return ctx
