from django.conf.urls.defaults import *
from guestbookapp.views import MainView, SignView


urlpatterns = patterns('',
    url(r"^sign/$", SignView.as_view(), name="sign"),
    url(r"^$", MainView.as_view(), name="main"),
)
