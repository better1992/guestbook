from django.conf.urls import patterns, url
from guestbookapp.views import MainView, SignView, \
	GreetingEditView, GreetingDeleteView, DojoView
from guestbookapp.api import GreetingCollectionView, GreetingSingleView


urlpatterns = patterns("",
					url(r"^sign/$", SignView.as_view(), name="sign"),
					url(r"^$", MainView.as_view(), name="main"),
					url(r"^edit/$", GreetingEditView.as_view(), name='edit'),
					url(r"^delete/$", GreetingDeleteView.as_view(), name='delete'),
					url(r'^api/guestbook/(?P<guestbook_name>[a-zA-Z0-9\s\+_]+)/greeting/$',
						GreetingCollectionView.as_view(), name='sign_api'),
					url(r'^api/guestbook/(?P<guestbook_name>(.)+)/greeting/(?P<id>(.)+)$',
						GreetingSingleView.as_view(), name="detail-greeting"),
					url(r'^dojo/?$', DojoView.as_view())
)
