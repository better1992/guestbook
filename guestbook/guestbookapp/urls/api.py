from django.conf.urls import patterns, url
from guestbookapp.views import DojoView
from guestbookapp.api import GreetingCollectionView, GreetingSingleView
from guestbookapp.forms import SignForm

urlpatterns = patterns("",
					url(r'^api/guestbook/(?P<guestbook_name>[a-zA-Z0-9\s\+_]+)/greeting/$',
						GreetingCollectionView.as_view(form_class=SignForm), name='sign_api'),
					url(r'^api/guestbook/(?P<guestbook_name>(.)+)/greeting/(?P<id>(.)+)$',
						GreetingSingleView.as_view(form_class=SignForm), name="detail-greeting"),
					url(r'^dojo/?$', DojoView.as_view())
)
