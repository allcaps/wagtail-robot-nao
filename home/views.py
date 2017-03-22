from django.urls import reverse
from django.views import View
from django.views.generic import FormView
from forms import StartForm


class StartView(FormView):
    form_class = StartForm
    template_name = "home/start.html"
    success_url = '/admin/login/?next=/admin/pages/add/home/homepage/3/'


class CredentialView(View):
    template_name = "home/credentials.html"
