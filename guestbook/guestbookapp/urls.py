from django.conf.urls.defaults import *
from guestbook.views import MainView, SignView

urlpatterns = patterns('',
    (r'^sign/$', SignView.as_view()),
    (r'^$', MainView.as_view()),
)