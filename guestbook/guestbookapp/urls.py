from django.conf.urls.defaults import *
from guestbookapp.views import MainView, SignView


urlpatterns = patterns('',
<<<<<<< HEAD
    url(r"^sign/$", SignView.as_view(),name="sign"),
    (r'^$', MainView.as_view()),
=======
    url(r"^sign/$", SignView.as_view(), name="sign"),
    url(r"^$", MainView.as_view(), name="main"),
>>>>>>> origin/feature/django-refactoring
)