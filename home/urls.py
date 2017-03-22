from django.conf.urls import url
from views import StartView, CredentialView

urlpatterns = [
    url(
        r'^start/$',
        StartView.as_view(),
        name='start'
    ),
    url(
        r'^credentials/',
        CredentialView.as_view(),
        name='credentials'
    ),

]
