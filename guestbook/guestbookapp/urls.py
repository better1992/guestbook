from django.conf.urls.defaults import *
from views import MainView, SignView, GreetingEditView, GreetingDeleteView


urlpatterns = patterns("",
                       url(r"^sign/$", SignView.as_view(), name="sign"),
                       url(r"^$", MainView.as_view(), name="main"),
                       url(r"^edit/$", GreetingEditView.as_view(), name='edit'),
                       url(r"^delete/$", GreetingDeleteView.as_view(), name='delete')
)
