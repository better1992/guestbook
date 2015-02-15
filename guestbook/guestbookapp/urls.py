from django.conf.urls.defaults import *
from guestbook.views import MainView, SignView

urlpatterns = patterns('',
    url(r"^sign/$", SignView.as_view(),name="sign"),
    (r'^$', MainView.as_view()),
)